import datetime as dt
import html
import re
import zipfile


OUT = "capabilities/fx-hedging/model.xlsx"
TABS = [
    "Cover", "Legend", "Inputs", "Forward", "Money Market", "Options",
    "Sensitivity", "Check", "Notes & Assumptions",
]
NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CHART = "http://schemas.openxmlformats.org/drawingml/2006/chart"
DRAW = "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing"
DRAW_A = "http://schemas.openxmlformats.org/drawingml/2006/main"

STYLE_TITLE = 1
STYLE_SECTION = 2
STYLE_HEADER = 3
STYLE_INPUT = 4
STYLE_ASSUMPTION = 5
STYLE_FORMULA = 6
STYLE_OUTPUT = 7
STYLE_NOTE = 8
STYLE_LABEL = 9
STYLE_DATE = 10
STYLE_MONEY = 11
STYLE_RATE = 12


def col_name(col):
    letters = ""
    while col:
        col, rem = divmod(col - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def ref(row, col):
    return f"{col_name(col)}{row}"


def esc(value):
    return html.escape(str(value), quote=False)


class Sheet:
    def __init__(self, title):
        self.title = title
        self.cells = {}
        self.widths = {}
        self.freeze = None
        self.filter = None

    def text(self, row, col, value, style=0):
        self.cells[(row, col)] = ("text", value, style)

    def number(self, row, col, value, style=0):
        self.cells[(row, col)] = ("number", value, style)

    def formula(self, row, col, formula, cached, style=STYLE_FORMULA):
        self.cells[(row, col)] = ("formula", formula.removeprefix("="), style, cached)

    def width(self, col, value):
        self.widths[col] = value


tabs = {tab: Sheet(tab) for tab in TABS}
names = {}
formulas = []
input_rows = [
    ("FC_AMT", "Foreign-currency receivable", "EUR", 6900000, "Invoice to the Portuguese buyer (ERP receivables ledger)"),
    ("S0_in", "Spot EUR/USD at inception", "USD per EUR", 1.1191, "EURUSD spot from one named provider; provider and timestamp pending Stage 4"),
    ("F0_in", "Quoted forward EUR/USD to settlement", "USD per EUR", 1.1705, "Bank indicative 182-day forward for the settlement date"),
    ("R_USD", "USD interest rate over the horizon", "Annual rate", 0.04216, "CME Term SOFR 6M"),
    ("R_FC", "EUR interest rate over the horizon", "Annual rate", 0.0296, "6-month Euribor fixing (EMMI / ECB)"),
    ("T_DAYS", "Days to settlement", "Days", 182, "Invoice due date minus VAL_DATE"),
    ("VAL_DATE", "Valuation date", "Date", dt.date(2026, 10, 29), "Date and time of the Stage 4 data pull"),
    ("BASIS", "Day-count denominator", "Days", 360, "CME Term SOFR and EMMI Euribor methodologies (ACT/360)"),
    ("K_PUT", "EUR put strike", "USD per EUR", None, "At-the-money placeholder linked to S0_in; confirm against bank quote"),
    ("K_CALL", "EUR call strike", "USD per EUR", None, "At-the-money placeholder linked to S0_in; confirm against bank quote"),
    ("PREM_PUT", "Put premium", "USD per EUR", 0.0194, "Bank quote for a 182-day at-the-money EUR put"),
    ("PREM_CALL", "Call premium", "USD per EUR", 0.0296, "Bank quote for a 182-day at-the-money EUR call"),
]
assumptions = [
    ("PARITY_TOLERANCE", 0.0005, "Maximum absolute parity gap percentage", "Fraction", "Project brief; spec §3"),
    ("STEP_FRAC", 0.01, "Settlement grid step as a fraction of S0_in", "Fraction", "Project brief"),
    ("GRID_HALF", 5, "Number of settlement steps on each side of spot", "Steps", "Project brief"),
]
named_input_set = {x[0] for x in input_rows}
assumption_values = {x[0]: x[1] for x in assumptions}


def add_title(sheet, title, subtitle, end=8):
    sheet.text(1, 1, title, STYLE_TITLE)
    sheet.text(2, 1, subtitle, STYLE_NOTE)
    for col in range(2, end + 1):
        sheet.text(1, col, "", STYLE_TITLE)


def section(sheet, row, title, end=6):
    for col in range(1, end + 1):
        sheet.text(row, col, title if col == 1 else "", STYLE_SECTION)


def header(sheet, row, values):
    for col, value in enumerate(values, 1):
        sheet.text(row, col, value, STYLE_HEADER)


def key(sheet):
    section(sheet, 2, "Color key", 15)
    for row, (label, style) in enumerate(
        [("Inputs — yellow", STYLE_INPUT), ("Assumptions — blue", STYLE_ASSUMPTION),
         ("Formulas — green", STYLE_FORMULA), ("Outputs — gray", STYLE_OUTPUT)],
        3,
    ):
        sheet.text(row, 14, label, STYLE_NOTE)
        sheet.text(row, 15, " ", style)
        sheet.width(14, 25)
        sheet.width(15, 5)


def add_name(name, sheet, row, col, end_row=None):
    start = f"${col_name(col)}${row}"
    if end_row is None:
        target = start
    else:
        target = f"{start}:${col_name(col)}${end_row}"
    names[name] = f"'{sheet}'!{target}"


def set_formula(sheet, row, col, formula, cached, style=STYLE_FORMULA):
    tabs[sheet].formula(row, col, formula, cached, style)
    formulas.append((sheet, row, col, formula.removeprefix("=")))


# Cover
cover = tabs["Cover"]
add_title(cover, "Scenario 12 — EUR Receivable Hedge Model", "US Grain Cooperative | Indicative model build | Specification v1.5")
section(cover, 4, "Scenario", 8)
for row, label, value in [
    (5, "Exposure", "EUR 6,900,000 receivable from a Portuguese feed manufacturer"),
    (6, "Settlement", "182 days; scenario due date: 29 April 2027"),
    (7, "Decision", "Compare forward, money-market, and EUR put hedge proceeds"),
    (8, "Author", "Meghan Hernandez"),
    (9, "Workbook date", dt.date(2026, 11, 13)),
    (10, "Specification version", "1.5"),
    (11, "Workbook tabs", ", ".join(TABS)),
]:
    cover.text(row, 1, label, STYLE_LABEL)
    if isinstance(value, dt.date):
        cover.number(row, 2, (value - dt.date(1899, 12, 30)).days, STYLE_DATE)
    else:
        cover.text(row, 2, value)
section(cover, 13, "Data provenance — values are indicative placeholders dated 29 Oct 2026", 8)
header(cover, 14, ["Named input", "Stage 4 source / provenance", "Status"])
for row, (name, description, unit, value, source) in enumerate(input_rows, 15):
    cover.text(row, 1, name, STYLE_LABEL)
    cover.text(row, 2, source)
    cover.text(row, 3, "Indicative placeholder; validate at Stage 4", STYLE_ASSUMPTION)
cover.text(28, 1, "Market-data status", STYLE_LABEL)
cover.text(28, 2, "Provider/access timestamps are not available yet. No Stage 4 quote is represented as sourced.")
cover.text(30, 1, "Further provenance", STYLE_LABEL)
cover.text(30, 2, "See Notes & Assumptions for the source log, timestamps pending Stage 4, and model constraints.")
cover.width(1, 25)
cover.width(2, 75)
cover.width(3, 43)

# Legend
legend = tabs["Legend"]
add_title(legend, "Workbook Legend", "Color convention is applied throughout every worksheet.")
header(legend, 4, ["Color", "Meaning", "Use"])
for row, (color, meaning, use, style) in enumerate([
    ("Yellow", "Inputs", "Scenario and market input cells on Inputs.", STYLE_INPUT),
    ("Blue", "Assumptions", "Named assumptions from §2.1.", STYLE_ASSUMPTION),
    ("Green", "Formulas", "Derived and intermediate calculations.", STYLE_FORMULA),
    ("Gray", "Outputs", "Strategy proceeds, sensitivity results, and check statuses.", STYLE_OUTPUT),
], 5):
    legend.text(row, 1, color, style)
    legend.text(row, 2, meaning, style)
    legend.text(row, 3, use, style)
section(legend, 11, "Workbook map", 6)
tab_purpose = [
    "Scenario and indicative provenance", "Color conventions", "Named inputs and derived factors",
    "Locked forward proceeds", "EUR borrowing, USD conversion, USD investment",
    "Put and call premiums/results", "Sensitivity table, winners, and chart",
    "Live numeric checks and manual audit notes", "Assumptions and Stage 4 source log",
]
for row, (tab, purpose) in enumerate(zip(TABS, tab_purpose), 12):
    legend.text(row, 1, tab, STYLE_LABEL)
    legend.text(row, 2, purpose)
legend.width(1, 28)
legend.width(2, 62)
legend.width(3, 68)

# Inputs and derived values
inputs = tabs["Inputs"]
add_title(inputs, "Inputs and Derived Values", "Indicative placeholders dated 29 Oct 2026; validate market data at Stage 4.")
section(inputs, 4, "Core inputs — yellow cells; named assumptions — blue cells", 6)
header(inputs, 5, ["Name", "Description", "Unit", "Value", "Stage 4 source"])
input_row_map = {}
for row, (name, desc, unit, value, source) in enumerate(input_rows, 6):
    input_row_map[name] = row
    inputs.text(row, 1, name, STYLE_LABEL)
    inputs.text(row, 2, desc)
    inputs.text(row, 3, unit)
    if name in ("K_PUT", "K_CALL"):
        set_formula("Inputs", row, 4, "S0_in", 1.1191)
        add_name(name, "Inputs", row, 4)
    else:
        if isinstance(value, dt.date):
            value = (value - dt.date(1899, 12, 30)).days
            style = STYLE_DATE
        else:
            style = STYLE_INPUT
        inputs.number(row, 4, value, style)
        add_name(name, "Inputs", row, 4)
    inputs.text(row, 5, source)

for row, (name, value, purpose, unit, source) in enumerate(assumptions, 18):
    inputs.text(row, 1, name, STYLE_LABEL)
    inputs.text(row, 2, purpose)
    inputs.text(row, 3, unit)
    inputs.number(row, 4, value, STYLE_ASSUMPTION)
    inputs.text(row, 5, source)
    add_name(name, "Inputs", row, 4)

section(inputs, 22, "Derived / intermediate values", 5)
header(inputs, 23, ["Name", "Description", "Unit", "Formula result", "Source"])
derived = [
    ("DF_USD", "USD maturity growth factor", "Factor", "1+R_USD*T_DAYS/BASIS", 1 + .04216 * 182 / 360),
    ("DF_FC", "EUR maturity growth factor", "Factor", "1+R_FC*T_DAYS/BASIS", 1 + .0296 * 182 / 360),
    ("FV_PREM_PUT", "Settlement-date value of put premium", "USD", "-PREM_PUT*FC_AMT*DF_USD", -.0194 * 6900000 * (1 + .04216 * 182 / 360)),
    ("FV_PREM_CALL", "Future value of call premium at settlement", "USD", "-PREM_CALL*FC_AMT*DF_USD", -.0296 * 6900000 * (1 + .04216 * 182 / 360)),
]
for row, (name, desc, unit, formula, cached) in enumerate(derived, 24):
    inputs.text(row, 1, name, STYLE_LABEL)
    inputs.text(row, 2, desc)
    inputs.text(row, 3, unit)
    set_formula("Inputs", row, 4, formula, cached)
    inputs.text(row, 5, "Calculated from named inputs")
    add_name(name, "Inputs", row, 4)
inputs.width(1, 25)
inputs.width(2, 43)
inputs.width(3, 19)
inputs.width(4, 24)
inputs.width(5, 76)
inputs.freeze = "A6"
inputs.filter = "A5:E20"

# Forward
forward = tabs["Forward"]
add_title(forward, "Forward Hedge", "Locks the USD value of the full EUR receivable.")
section(forward, 4, "Forward proceeds", 5)
header(forward, 5, ["Metric", "Value", "Unit", "Calculation"])
for row, label, formula, cached, unit in [
    (6, "Receivable", "FC_AMT", 6900000, "EUR"),
    (7, "Quoted forward rate", "F0_in", 1.1705, "USD per EUR"),
    (8, "Locked forward proceeds", "FC_AMT*F0_in", 8076450, "USD"),
]:
    forward.text(row, 1, label, STYLE_LABEL)
    set_formula("Forward", row, 2, formula, cached, STYLE_OUTPUT if row == 8 else STYLE_FORMULA)
    forward.text(row, 3, unit)
    forward.text(row, 4, "FC_AMT × F0_in" if row == 8 else "Named input")
add_name("USD_FWD", "Forward", 8, 2)
forward.text(10, 1, "Cash timing", STYLE_LABEL)
forward.text(10, 2, "No stated upfront premium; proceeds are constant across settlement-rate scenarios.")
forward.width(1, 37)
forward.width(2, 25)
forward.width(3, 21)
forward.width(4, 38)

# Money-market hedge
mm = tabs["Money Market"]
add_title(mm, "Money-Market Hedge", "Three separate cash-flow legs using the stated simple-interest day-count convention.")
section(mm, 4, "Hedge mechanics", 5)
header(mm, 5, ["Leg", "Amount", "Unit", "Formula"])
mm_formulas = [
    (6, "EUR borrowing at inception", "FC_AMT/DF_FC", 6900000 / (1 + .0296 * 182 / 360), "EUR"),
    (7, "USD conversion at spot", "(FC_AMT/DF_FC)*S0_in", 6900000 / (1 + .0296 * 182 / 360) * 1.1191, "USD"),
    (8, "USD investment at settlement", "(FC_AMT/DF_FC)*S0_in*DF_USD",
     6900000 / (1 + .0296 * 182 / 360) * 1.1191 * (1 + .04216 * 182 / 360), "USD"),
]
for row, label, formula, cached, unit in mm_formulas:
    mm.text(row, 1, label, STYLE_LABEL)
    set_formula("Money Market", row, 2, formula, cached, STYLE_OUTPUT)
    mm.text(row, 3, unit)
    mm.text(row, 4, formula)
mm.text(10, 1, "Money-market proceeds", STYLE_LABEL)
set_formula("Money Market", 10, 2, "(FC_AMT/DF_FC)*S0_in*DF_USD", mm_formulas[2][3], STYLE_OUTPUT)
mm.text(10, 3, "USD")
mm.text(10, 4, "USD investment carried to settlement")
add_name("USD_MM", "Money Market", 10, 2)
section(mm, 13, "Parity comparison", 5)
mm.text(14, 1, "Forward proceeds", STYLE_LABEL)
set_formula("Money Market", 14, 2, "USD_FWD", 8076450, STYLE_OUTPUT)
mm.text(14, 3, "USD")
mm.text(15, 1, "Absolute dollar gap", STYLE_LABEL)
set_formula("Money Market", 15, 2, "ABS(USD_FWD-USD_MM)", abs(8076450 - mm_formulas[2][3]), STYLE_OUTPUT)
mm.text(15, 3, "USD")
mm.text(16, 1, "Signed gap percentage", STYLE_LABEL)
set_formula("Money Market", 16, 2, "(USD_FWD-USD_MM)/USD_MM", (8076450 - mm_formulas[2][3]) / mm_formulas[2][3], STYLE_OUTPUT)
mm.text(16, 3, "Fraction")
mm.text(17, 1, "Parity status", STYLE_LABEL)
set_formula("Money Market", 17, 2, 'IF(ABS((USD_FWD-USD_MM)/USD_MM)<=PARITY_TOLERANCE,"PASS","REVIEW")', "REVIEW", STYLE_OUTPUT)
mm.text(17, 3, "PASS / REVIEW")
mm.width(1, 44)
mm.width(2, 26)
mm.width(3, 20)
mm.width(4, 44)

# Options
options = tabs["Options"]
add_title(options, "Option Hedge Reference", "Premium is paid upfront and carried forward at the USD rate.")
section(options, 4, "EUR put", 5)
header(options, 5, ["Metric", "Amount", "Unit", "Calculation"])
option_rows = [
    (6, "Put premium paid upfront", "PREM_PUT*FC_AMT", .0194 * 6900000, "USD", "Positive cash paid at inception"),
    (7, "Put premium at settlement", "FV_PREM_PUT", -.0194 * 6900000 * (1 + .04216 * 182 / 360), "USD", "Negative future value"),
    (8, "Put proceeds at spot", "MAX(S0_in,K_PUT)*FC_AMT+FV_PREM_PUT",
     1.1191 * 6900000 - .0194 * 6900000 * (1 + .04216 * 182 / 360), "USD", "Put proceeds at S_T = S0_in"),
    (9, "Put floor across sensitivity grid", "MIN(USD_PUT)",
     1.1191 * 6900000 - .0194 * 6900000 * (1 + .04216 * 182 / 360), "USD", "Minimum across the formula-driven grid"),
]
for row, label, formula, cached, unit, detail in option_rows:
    options.text(row, 1, label, STYLE_LABEL)
    set_formula("Options", row, 2, formula, cached, STYLE_OUTPUT)
    options.text(row, 3, unit)
    options.text(row, 4, detail)
add_name("USD_FLOOR_PUT", "Options", 9, 2)
section(options, 12, "EUR call reference leg (not one of the four charted strategies)", 6)
header(options, 13, ["Metric", "Amount", "Unit", "Calculation"])
call_rows = [
    (14, "Call premium paid upfront", "PREM_CALL*FC_AMT", .0296 * 6900000, "USD", "Positive cash paid at inception"),
    (15, "Call premium at settlement", "FV_PREM_CALL", -.0296 * 6900000 * (1 + .04216 * 182 / 360), "USD", "Negative future value"),
    (16, "Call net at spot", "MAX(0,S0_in-K_CALL)*FC_AMT+FV_PREM_CALL",
     -.0296 * 6900000 * (1 + .04216 * 182 / 360), "USD", "Call result at S_T = S0_in"),
    (17, "Call break-even rate", "K_CALL-FV_PREM_CALL/FC_AMT",
     1.1191 - (-.0296 * 6900000 * (1 + .04216 * 182 / 360)) / 6900000, "USD per EUR", "K_CALL − FV_PREM_CALL / FC_AMT"),
]
for row, label, formula, cached, unit, detail in call_rows:
    options.text(row, 1, label, STYLE_LABEL)
    set_formula("Options", row, 2, formula, cached, STYLE_OUTPUT)
    options.text(row, 3, unit)
    options.text(row, 4, detail)
options.width(1, 45)
options.width(2, 27)
options.width(3, 19)
options.width(4, 50)

# Sensitivity table. Only the complete named grid/series ranges are named; no individual rows.
sense = tabs["Sensitivity"]
add_title(sense, "Settlement-Rate Sensitivity", "Deterministic grid; four proceeds strategies are charted. Call is a reference leg only.", 12)
section(sense, 4, "Base-case strategy summary (S_T = S0_in)", 5)
header(sense, 5, ["Strategy / metric", "USD proceeds"])
summary = [
    (6, "No hedge at spot", "S0_in*FC_AMT", 1.1191 * 6900000),
    (7, "Forward", "USD_FWD", 8076450),
    (8, "Money market", "USD_MM", mm_formulas[2][3]),
    (9, "EUR put at spot", "MAX(S0_in,K_PUT)*FC_AMT+FV_PREM_PUT",
     1.1191 * 6900000 - .0194 * 6900000 * (1 + .04216 * 182 / 360)),
    (10, "EUR put floor", "USD_FLOOR_PUT",
     1.1191 * 6900000 - .0194 * 6900000 * (1 + .04216 * 182 / 360)),
]
for row, label, formula, cached in summary:
    sense.text(row, 1, label, STYLE_LABEL)
    set_formula("Sensitivity", row, 2, formula, cached, STYLE_OUTPUT)
header(sense, 13, [
    "Settlement EUR/USD", "No hedge (USD)", "Forward (USD)", "Money market (USD)",
    "EUR put (USD)", "Call net (reference, USD)", "Forward hedge profit",
    "Money-market hedge profit", "Put hedge profit", "Overall winner", "Best active hedge",
])
data_start, data_end = 14, 24
add_name("S_T_grid", "Sensitivity", data_start, 1, data_end)
add_name("USD_NO_HEDGE", "Sensitivity", data_start, 2, data_end)
add_name("USD_PUT", "Sensitivity", data_start, 5, data_end)
grid_cache = []
for row in range(data_start, data_end + 1):
    k = row - data_start - 5
    st = 1.1191 * (1 + k * .01)
    idx = f"ROW()-MIN(ROW(S_T_grid))+1"
    st_here = f"INDEX(S_T_grid,{idx})"
    no_hedge = st * 6900000
    fwd = 8076450
    money = mm_formulas[2][3]
    put = max(st, 1.1191) * 6900000 - .0194 * 6900000 * (1 + .04216 * 182 / 360)
    call = max(0, st - 1.1191) * 6900000 - .0296 * 6900000 * (1 + .04216 * 182 / 360)
    formulas_row = [
        (1, "S0_in*(1+(ROW()-MIN(ROW(S_T_grid))-GRID_HALF)*STEP_FRAC)", st, STYLE_FORMULA),
        (2, f"{st_here}*FC_AMT", no_hedge, STYLE_MONEY),
        (3, "USD_FWD", fwd, STYLE_MONEY),
        (4, "USD_MM", money, STYLE_MONEY),
        (5, f"MAX({st_here},K_PUT)*FC_AMT+FV_PREM_PUT", put, STYLE_MONEY),
        (6, f"MAX(0,{st_here}-K_CALL)*FC_AMT+FV_PREM_CALL", call, STYLE_MONEY),
        (7, f"USD_FWD-{st_here}*FC_AMT", fwd - no_hedge, STYLE_MONEY),
        (8, f"USD_MM-{st_here}*FC_AMT", money - no_hedge, STYLE_MONEY),
        (9, f"MAX({st_here},K_PUT)*FC_AMT+FV_PREM_PUT-{st_here}*FC_AMT", put - no_hedge, STYLE_MONEY),
    ]
    for col, formula, cached, style in formulas_row:
        set_formula("Sensitivity", row, col, formula, cached, style)
    max_all = max(no_hedge, fwd, money, put)
    winner = "No hedge" if no_hedge == max_all else "Forward" if fwd == max_all else "Money market" if money == max_all else "EUR put"
    max_hedges = max(fwd, money, put)
    best = "Forward" if fwd == max_hedges else "Money market" if money == max_hedges else "EUR put"
    winner_formula = (
        f'IF({st_here}*FC_AMT=MAX({st_here}*FC_AMT,USD_FWD,USD_MM,MAX({st_here},K_PUT)*FC_AMT+FV_PREM_PUT),"No hedge",'
        f'IF(USD_FWD=MAX({st_here}*FC_AMT,USD_FWD,USD_MM,MAX({st_here},K_PUT)*FC_AMT+FV_PREM_PUT),"Forward",'
        f'IF(USD_MM=MAX({st_here}*FC_AMT,USD_FWD,USD_MM,MAX({st_here},K_PUT)*FC_AMT+FV_PREM_PUT),"Money market","EUR put")))'
    )
    best_formula = (
        f'IF(USD_FWD=MAX(USD_FWD,USD_MM,MAX({st_here},K_PUT)*FC_AMT+FV_PREM_PUT),"Forward",'
        f'IF(USD_MM=MAX(USD_FWD,USD_MM,MAX({st_here},K_PUT)*FC_AMT+FV_PREM_PUT),"Money market","EUR put"))'
    )
    set_formula("Sensitivity", row, 10, winner_formula, winner, STYLE_OUTPUT)
    set_formula("Sensitivity", row, 11, best_formula, best, STYLE_OUTPUT)
    grid_cache.append((st, no_hedge, fwd, money, put, call))
sense.width(1, 23)
for col in range(2, 10):
    sense.width(col, 23)
sense.width(10, 23)
sense.width(11, 22)
sense.freeze = "A14"
sense.filter = "A13:K24"

# Provenance/assumptions
notes = tabs["Notes & Assumptions"]
add_title(notes, "Notes & Assumptions", "Model constraints, named assumptions, and Stage 4 market-data provenance.", 9)
section(notes, 4, "Named assumptions from §2.1 (blue cells)", 6)
header(notes, 5, ["Name", "Value", "Purpose", "Source"])
for row, (name, value, purpose, unit, source) in enumerate(assumptions, 6):
    notes.text(row, 1, name, STYLE_LABEL)
    notes.number(row, 2, value, STYLE_ASSUMPTION)
    notes.text(row, 3, purpose)
    notes.text(row, 4, source)
section(notes, 11, "Market-data source and access log", 6)
header(notes, 12, ["Name", "Unit", "Source / provider", "Access timestamp", "Value status"])
for row, (name, desc, unit, value, source) in enumerate(input_rows, 13):
    notes.text(row, 1, name, STYLE_LABEL)
    notes.text(row, 2, unit)
    notes.text(row, 3, source)
    notes.text(row, 4, "Not available — populate at Stage 4")
    notes.text(row, 5, "Indicative placeholder dated 29 Oct 2026", STYLE_ASSUMPTION)
section(notes, 27, "Assumptions and limitations", 6)
for row, text in enumerate([
    "EUR/USD is USD per EUR; higher settlement rates increase USD proceeds on the receivable.",
    "Static full-notional EUR receivable; single maturity; partial, layered, and dynamic hedging are outside scope.",
    "Both money-market legs use simple interest with the named ACT/360 basis and 182-day placeholder horizon.",
    "Forward locks the quoted rate and has no stated upfront premium.",
    "Money-market hedge borrows the EUR present value, converts at spot, and invests USD to settlement.",
    "Option premium is paid upfront and carried to settlement at R_USD; call is a reference leg, not a chart strategy.",
    "Base case excludes bid-ask spreads, transaction costs, taxes, accounting treatment, credit/counterparty, and settlement risk.",
    "Settlement-rate scenarios are deterministic; no probabilities or implied-volatility distribution are used.",
    "All market inputs remain indicative pending source/provider validation and Stage 4 timestamps.",
], 28):
    notes.text(row, 1, text, STYLE_NOTE)
notes.width(1, 34)
notes.width(2, 22)
notes.width(3, 78)
notes.width(4, 53)
notes.width(5, 48)
notes.freeze = "A6"

# Live numeric §6.3 checks; reference figures are typed from the specification.
check = tabs["Check"]
add_title(check, "Live Model Checks", "Numeric checks compare live formulas with typed §6.3 reference figures.", 7)
header(check, 4, ["§6.3 check", "Live result", "Status", "Typed spec reference / interpretation"])

def check_row(row, label, result_formula, cached, expected, status_formula, status, style=STYLE_OUTPUT):
    check.text(row, 1, label, STYLE_LABEL)
    set_formula("Check", row, 2, result_formula, cached, style)
    set_formula("Check", row, 3, status_formula, status, STYLE_OUTPUT)
    check.text(row, 4, expected)

check_row(5, "Required §2.1 named inputs and assumptions", "COUNTA(FC_AMT,S0_in,F0_in,R_USD,R_FC,T_DAYS,VAL_DATE,BASIS,K_PUT,K_CALL,PREM_PUT,PREM_CALL,PARITY_TOLERANCE,STEP_FRAC,GRID_HALF)",
          15, "15 names: 12 core inputs plus 3 named assumptions",
          'IF(COUNTA(FC_AMT,S0_in,F0_in,R_USD,R_FC,T_DAYS,VAL_DATE,BASIS,K_PUT,K_CALL,PREM_PUT,PREM_CALL,PARITY_TOLERANCE,STEP_FRAC,GRID_HALF)=15,"PASS","FAIL")',
          "PASS")
check_row(6, "FC_AMT", "FC_AMT", 6900000, "EUR 6,900,000",
          'IF(ABS(FC_AMT-6900000)<=1,"PASS","FAIL")', "PASS", STYLE_MONEY)
check_row(7, "T_DAYS", "T_DAYS", 182, "182 days",
          'IF(ABS(T_DAYS-182)<=1,"PASS","FAIL")', "PASS", STYLE_OUTPUT)
check_row(8, "Forward proceeds", "USD_FWD", 8076450, "USD 8,076,450",
          'IF(ABS(USD_FWD-8076450)<=1,"PASS","FAIL")', "PASS", STYLE_MONEY)
check_row(9, "Money-market EUR borrowing", "FC_AMT/DF_FC", mm_formulas[0][3], "EUR 6,798,268",
          'IF(ABS(FC_AMT/DF_FC-6798268)<=1,"PASS","FAIL")', "PASS", STYLE_MONEY)
check_row(10, "Money-market USD conversion", "(FC_AMT/DF_FC)*S0_in", mm_formulas[1][3], "USD 7,607,941",
          'IF(ABS((FC_AMT/DF_FC)*S0_in-7607941)<=1,"PASS","FAIL")', "PASS", STYLE_MONEY)
check_row(11, "Money-market USD investment", "USD_MM", mm_formulas[2][3], "USD 7,770,099",
          'IF(ABS(USD_MM-7770099)<=1,"PASS","FAIL")', "PASS", STYLE_MONEY)
check_row(12, "Put proceeds at strike", "MAX(K_PUT,K_PUT)*FC_AMT+FV_PREM_PUT",
          1.1191 * 6900000 - .0194 * 6900000 * (1 + .04216 * 182 / 360), "USD 7,585,077",
          'IF(ABS(MAX(K_PUT,K_PUT)*FC_AMT+FV_PREM_PUT-7585077)<=1,"PASS","FAIL")', "PASS", STYLE_MONEY)
check_row(13, "Put premium future value", "FV_PREM_PUT", -.0194 * 6900000 * (1 + .04216 * 182 / 360),
          "USD -136,713",
          'IF(ABS(FV_PREM_PUT-(-136713))<=1,"PASS","FAIL")', "PASS", STYLE_MONEY)
check_row(14, "Call premium future value", "FV_PREM_CALL", -.0296 * 6900000 * (1 + .04216 * 182 / 360),
          "USD -208,593",
          'IF(ABS(FV_PREM_CALL-(-208593))<=1,"PASS","FAIL")', "PASS", STYLE_MONEY)
check_row(15, "Call net at or below strike", "MAX(0,K_CALL-K_CALL)*FC_AMT+FV_PREM_CALL",
          -.0296 * 6900000 * (1 + .04216 * 182 / 360), "USD -208,593",
          'IF(ABS(MAX(0,K_CALL-K_CALL)*FC_AMT+FV_PREM_CALL-(-208593))<=1,"PASS","FAIL")',
          "PASS", STYLE_MONEY)
call_upper_formula = "MAX(0,S0_in*(1+GRID_HALF*STEP_FRAC)-K_CALL)*FC_AMT+FV_PREM_CALL"
call_upper = max(0, 1.1191 * (1 + 5 * .01) - 1.1191) * 6900000 - .0296 * 6900000 * (1 + .04216 * 182 / 360)
check_row(16, "Call net at +5%", call_upper_formula, call_upper, "USD 177,496",
          f'IF(ABS({call_upper_formula}-177496)<=1,"PASS","FAIL")', "PASS", STYLE_MONEY)
be_formula = "K_CALL-FV_PREM_CALL/FC_AMT"
be_value = 1.1191 - (-.0296 * 6900000 * (1 + .04216 * 182 / 360)) / 6900000
check_row(17, "Call break-even rate", be_formula, be_value, "1.1493 USD per EUR",
          f'IF(ABS({be_formula}-1.1493)<=0.0001,"PASS","FAIL")', "PASS", STYLE_RATE)
check_row(18, "Absolute parity gap", "ABS(USD_FWD-USD_MM)", abs(8076450 - mm_formulas[2][3]),
          "USD 306,351",
          'IF(ABS(ABS(USD_FWD-USD_MM)-306351)<=1,"PASS","FAIL")', "PASS", STYLE_MONEY)
gap_pct = (8076450 - mm_formulas[2][3]) / mm_formulas[2][3]
check_row(19, "Parity gap percentage", "(USD_FWD-USD_MM)/USD_MM", gap_pct, "3.94%; expected REVIEW",
          'IF(AND(ABS((USD_FWD-USD_MM)/USD_MM-0.0394)<=0.0001,ABS((USD_FWD-USD_MM)/USD_MM)>PARITY_TOLERANCE),"PASS","FAIL")',
          "PASS", STYLE_RATE)
check_row(20, "Parity status (absolute-value test)", 'IF(ABS((USD_FWD-USD_MM)/USD_MM)<=PARITY_TOLERANCE,"PASS","REVIEW")',
          "REVIEW", "REVIEW with indicative placeholders",
          'IF(ABS((USD_FWD-USD_MM)/USD_MM)>PARITY_TOLERANCE,"REVIEW","PASS")', "REVIEW")
check_row(21, "Grid populated value count", "COUNT(S_T_grid)", 11, "11 populated values; formula cells verified below",
          'IF(COUNT(S_T_grid)=11,"PASS","FAIL")', "PASS")
check_row(22, "Grid lower endpoint", "INDEX(S_T_grid,1)", grid_cache[0][0], "1.0631 ± 0.0001",
          'IF(ABS(INDEX(S_T_grid,1)-1.0631)<=0.0001,"PASS","FAIL")', "PASS", STYLE_RATE)
check_row(23, "Grid upper endpoint", "INDEX(S_T_grid,ROWS(S_T_grid))", grid_cache[-1][0], "1.1751 ± 0.0001",
          'IF(ABS(INDEX(S_T_grid,ROWS(S_T_grid))-1.1751)<=0.0001,"PASS","FAIL")', "PASS", STYLE_RATE)
section(check, 25, "Manual verification (non-numeric checklist items)", 6)
for row, label, result in [
    (26, "Formula rows, references, and defined-name scope", "Build audit confirms all 11 grid rows contain formulas; formulas use only allowed names and contain no bare cell references."),
    (27, "Color legend on every tab", "Manually verified; yellow inputs, blue assumptions, green formulas, gray outputs."),
    (28, "Market source/provider and access timestamps", "Manually verified; Stage 4 access timestamps are unavailable, so placeholders are explicitly marked pending."),
]:
    check.text(row, 1, label, STYLE_LABEL)
    check.text(row, 2, result, STYLE_NOTE)
check.width(1, 46)
check.width(2, 40)
check.width(3, 17)
check.width(4, 53)
check.freeze = "A5"
check.filter = "A4:D23"

# Color key on all tabs.
for sheet in tabs.values():
    key(sheet)

# Formula audit: worksheet formulae must use allowed defined names, and contain no
# numeric constants other than 0 and 1, except typed reference checks on Check.
functions = {
    "IF", "ABS", "COUNTA", "MAX", "MIN", "ROW", "INDEX", "SUMPRODUCT",
    "ROWS", "AND", "COUNT",
}
token_re = re.compile(r'"(?:[^"]|"")*"|[A-Za-z_][A-Za-z0-9_.]*|[0-9]+(?:\.[0-9]+)?')
cell_ref_re = re.compile(r"(?<![A-Za-z0-9_])\$?[A-Z]{1,3}\$?[0-9]+(?![A-Za-z0-9_])")
bad = []
for sheet, row, col, formula in formulas:
    numeric_tokens = []
    for token in token_re.findall(formula):
        if token.startswith('"'):
            continue
        if re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", token):
            numeric_tokens.append(token)
            continue
        if token.upper() in functions or token in names:
            continue
        bad.append((sheet, ref(row, col), f"unknown token {token}"))
    if cell_ref_re.search(formula):
        bad.append((sheet, ref(row, col), "cell reference"))
    if sheet != "Check" and any(n not in ("0", "1") for n in numeric_tokens):
        bad.append((sheet, ref(row, col), f"numeric literal(s) {numeric_tokens}"))
    if not any(token in names for token in token_re.findall(formula) if not token.startswith('"')):
        bad.append((sheet, ref(row, col), "no named range"))
if bad:
    raise ValueError(f"Formula audit failed: {bad[:12]}")
grid_formula_rows = [
    (sheet, row, col)
    for sheet, row, col, formula in formulas
    if sheet == "Sensitivity" and col == 1 and 14 <= row <= 24
]
if len(grid_formula_rows) != 11:
    raise ValueError(f"Expected 11 formula-driven sensitivity rows; found {len(grid_formula_rows)}")


def cell_xml(addr, cell):
    kind, value, style = cell[:3]
    if kind == "text":
        return f'<c r="{addr}" s="{style}" t="inlineStr"><is><t xml:space="preserve">{esc(value)}</t></is></c>'
    if kind == "number":
        return f'<c r="{addr}" s="{style}"><v>{value}</v></c>'
    cached = cell[3]
    if isinstance(cached, str):
        return f'<c r="{addr}" s="{style}" t="str"><f>{esc(value)}</f><v>{esc(cached)}</v></c>'
    return f'<c r="{addr}" s="{style}"><f>{esc(value)}</f><v>{cached:.15g}</v></c>'


def worksheet_xml(sheet, drawing=False):
    max_row = max((r for r, c in sheet.cells), default=1)
    max_col = max((c for r, c in sheet.cells), default=1)
    xml = [f'<worksheet xmlns="{NS}" xmlns:r="{REL}"><dimension ref="A1:{ref(max_row,max_col)}"/>']
    xml.append('<sheetViews><sheetView workbookViewId="0">')
    if sheet.freeze:
        m = re.match(r"([A-Z]+)(\d+)", sheet.freeze)
        col = 0
        for letter in m.group(1):
            col = col * 26 + ord(letter) - 64
        row = int(m.group(2))
        xml.append(f'<pane xSplit="{col-1}" ySplit="{row-1}" topLeftCell="{sheet.freeze}" activePane="bottomRight" state="frozen"/>')
    xml.append("</sheetView></sheetViews><cols>")
    for col, width in sorted(sheet.widths.items()):
        xml.append(f'<col min="{col}" max="{col}" width="{width}" customWidth="1"/>')
    xml.append("</cols><sheetData>")
    for row in range(1, max_row + 1):
        cols = sorted(c for r, c in sheet.cells if r == row)
        if not cols:
            continue
        xml.append(f'<row r="{row}">')
        xml.extend(cell_xml(ref(row, col), sheet.cells[(row, col)]) for col in cols)
        xml.append("</row>")
    xml.append("</sheetData>")
    if sheet.filter:
        xml.append(f'<autoFilter ref="{sheet.filter}"/>')
    if drawing:
        xml.append('<drawing r:id="rId1"/>')
    xml.append("</worksheet>")
    return "".join(xml)


def styles_xml():
    fonts = [
        '<font><sz val="10"/><name val="Aptos"/><color rgb="FF222222"/></font>',
        '<font><b/><sz val="16"/><name val="Aptos Display"/><color rgb="FF17365D"/></font>',
        '<font><b/><sz val="10"/><name val="Aptos"/><color rgb="FFFFFFFF"/></font>',
        '<font><b/><sz val="10"/><name val="Aptos"/><color rgb="FF222222"/></font>',
    ]
    fills = ['<fill><patternFill patternType="none"/></fill>', '<fill><patternFill patternType="gray125"/></fill>']
    for color in ("FF17365D", "FFFFE699", "FFD9EAF7", "FFD9EAD3", "FFD9D9D9"):
        fills.append(f'<fill><patternFill patternType="solid"><fgColor rgb="{color}"/><bgColor indexed="64"/></patternFill></fill>')
    borders = [
        '<border><left/><right/><top/><bottom/><diagonal/></border>',
        '<border><left style="thin"><color rgb="FFD9E1F2"/></left><right style="thin"><color rgb="FFD9E1F2"/></right><top style="thin"><color rgb="FFD9E1F2"/></top><bottom style="thin"><color rgb="FFD9E1F2"/></bottom><diagonal/></border>',
    ]
    xfs = [
        '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>',
        '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>',
        '<xf numFmtId="0" fontId="2" fillId="2" borderId="1" xfId="0" applyFill="1" applyFont="1" applyBorder="1"/>',
        '<xf numFmtId="0" fontId="2" fillId="2" borderId="1" xfId="0" applyFill="1" applyFont="1" applyBorder="1" applyAlignment="1"><alignment wrapText="1" vertical="center"/></xf>',
        '<xf numFmtId="0" fontId="0" fillId="3" borderId="1" xfId="0" applyFill="1" applyBorder="1"/>',
        '<xf numFmtId="0" fontId="0" fillId="4" borderId="1" xfId="0" applyFill="1" applyBorder="1"/>',
        '<xf numFmtId="0" fontId="0" fillId="5" borderId="1" xfId="0" applyFill="1" applyBorder="1"/>',
        '<xf numFmtId="0" fontId="0" fillId="6" borderId="1" xfId="0" applyFill="1" applyBorder="1"/>',
        '<xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>',
        '<xf numFmtId="0" fontId="3" fillId="0" borderId="0" xfId="0" applyFont="1"/>',
        '<xf numFmtId="14" fontId="0" fillId="3" borderId="1" xfId="0" applyNumberFormat="1" applyFill="1" applyBorder="1"/>',
        '<xf numFmtId="4" fontId="0" fillId="6" borderId="1" xfId="0" applyNumberFormat="1" applyFill="1" applyBorder="1"/>',
        '<xf numFmtId="10" fontId="0" fillId="6" borderId="1" xfId="0" applyNumberFormat="1" applyFill="1" applyBorder="1"/>',
    ]
    return (
        f'<styleSheet xmlns="{NS}"><numFmts count="0"/>'
        f'<fonts count="{len(fonts)}">{"".join(fonts)}</fonts>'
        f'<fills count="{len(fills)}">{"".join(fills)}</fills>'
        f'<borders count="{len(borders)}">{"".join(borders)}</borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        f'<cellXfs count="{len(xfs)}">{"".join(xfs)}</cellXfs>'
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>'
    )


def chart_xml():
    series_specs = [("No hedge", "B", "4472C4"), ("Forward", "C", "ED7D31"),
                    ("Money market", "D", "A5A5A5"), ("EUR put", "E", "70AD47")]
    series = []
    for i, (title, col, color) in enumerate(series_specs):
        series.append(
            f'<c:ser><c:idx val="{i}"/><c:order val="{i}"/><c:tx><c:v>{title}</c:v></c:tx>'
            f'<c:spPr><a:ln w="28575"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:ln></c:spPr>'
            '<c:marker><c:symbol val="circle"/><c:size val="5"/></c:marker>'
            '<c:cat><c:numRef><c:f>S_T_grid</c:f></c:numRef></c:cat>'
            f'<c:val><c:numRef><c:f>\'Sensitivity\'!${col}$14:${col}$24</c:f></c:numRef></c:val></c:ser>'
        )
    return (
        f'<c:chartSpace xmlns:c="{CHART}" xmlns:a="{DRAW_A}"><c:lang val="en-US"/>'
        '<c:chart><c:title><c:tx><c:rich><a:bodyPr/><a:lstStyle/><a:p><a:r><a:rPr lang="en-US" sz="1400" b="1"/>'
        '<a:t>USD proceeds by settlement EUR/USD</a:t></a:r></a:p></c:rich></c:tx></c:title>'
        '<c:plotArea><c:lineChart><c:grouping val="standard"/><c:varyColors val="0"/>'
        + "".join(series)
        + '<c:axId val="12345601"/><c:axId val="12345602"/></c:lineChart>'
        '<c:catAx><c:axId val="12345601"/><c:scaling><c:orientation val="minMax"/></c:scaling><c:delete val="0"/><c:axPos val="b"/>'
        '<c:title><c:tx><c:rich><a:bodyPr/><a:lstStyle/><a:p><a:r><a:rPr lang="en-US"/><a:t>Settlement EUR/USD (USD per EUR)</a:t></a:r></a:p></c:rich></c:tx></c:title><c:crossAx val="12345602"/></c:catAx>'
        '<c:valAx><c:axId val="12345602"/><c:scaling><c:orientation val="minMax"/></c:scaling><c:delete val="0"/><c:axPos val="l"/>'
        '<c:numFmt formatCode="$#,##0" sourceLinked="0"/><c:title><c:tx><c:rich><a:bodyPr/><a:lstStyle/><a:p><a:r><a:rPr lang="en-US"/><a:t>USD proceeds</a:t></a:r></a:p></c:rich></c:tx></c:title><c:crossAx val="12345601"/></c:valAx>'
        '</c:plotArea><c:legend><c:legendPos val="b"/></c:legend><c:plotVisOnly val="1"/></c:chart></c:chartSpace>'
    )


def workbook_xml():
    sheet_nodes = "".join(
        f'<sheet name="{html.escape(tab, quote=True)}" sheetId="{i}" r:id="rId{i}"/>'
        for i, tab in enumerate(TABS, 1)
    )
    defined_nodes = "".join(
        f'<definedName name="{html.escape(name, quote=True)}">{esc(value)}</definedName>'
        for name, value in names.items()
    )
    return (
        f'<workbook xmlns="{NS}" xmlns:r="{REL}"><bookViews><workbookView/></bookViews>'
        f'<sheets>{sheet_nodes}</sheets><definedNames>{defined_nodes}</definedNames>'
        '<calcPr calcId="191029" calcMode="auto" fullCalcOnLoad="1" forceFullCalc="1"/></workbook>'
    )


def drawing_xml():
    return (
        f'<xdr:wsDr xmlns:xdr="{DRAW}" xmlns:a="{DRAW_A}">'
        '<xdr:twoCellAnchor><xdr:from><xdr:col>12</xdr:col><xdr:colOff>0</xdr:colOff><xdr:row>12</xdr:row><xdr:rowOff>0</xdr:rowOff></xdr:from>'
        '<xdr:to><xdr:col>23</xdr:col><xdr:colOff>0</xdr:colOff><xdr:row>31</xdr:row><xdr:rowOff>0</xdr:rowOff></xdr:to>'
        '<xdr:graphicFrame macro=""><xdr:nvGraphicFramePr><xdr:cNvPr id="2" name="Sensitivity line chart"/>'
        '<xdr:cNvGraphicFramePr/></xdr:nvGraphicFramePr><xdr:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/></xdr:xfrm>'
        f'<a:graphic><a:graphicData uri="{CHART}"><c:chart xmlns:c="{CHART}" xmlns:r="{REL}" r:id="rId1"/></a:graphicData></a:graphic>'
        '</xdr:graphicFrame><xdr:clientData/></xdr:twoCellAnchor></xdr:wsDr>'
    )


root_rels = f'<Relationships xmlns="{PKG_REL}"><Relationship Id="rId1" Type="{REL}/officeDocument" Target="xl/workbook.xml"/></Relationships>'
wb_rels = (
    f'<Relationships xmlns="{PKG_REL}">'
    + "".join(f'<Relationship Id="rId{i}" Type="{REL}/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1, 10))
    + f'<Relationship Id="rId10" Type="{REL}/styles" Target="styles.xml"/></Relationships>'
)
sheet_drawing_rels = f'<Relationships xmlns="{PKG_REL}"><Relationship Id="rId1" Type="{REL}/drawing" Target="../drawings/drawing1.xml"/></Relationships>'
drawing_rels = f'<Relationships xmlns="{PKG_REL}"><Relationship Id="rId1" Type="{REL}/chart" Target="../charts/chart1.xml"/></Relationships>'
content_types = (
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
    '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
    + "".join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1, 10))
    + '<Override PartName="/xl/drawings/drawing1.xml" ContentType="application/vnd.openxmlformats-officedocument.drawing+xml"/>'
    '<Override PartName="/xl/charts/chart1.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.chart+xml"/>'
    '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
    '</Types>'
)

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", root_rels)
    z.writestr("xl/workbook.xml", workbook_xml())
    z.writestr("xl/_rels/workbook.xml.rels", wb_rels)
    z.writestr("xl/styles.xml", styles_xml())
    for i, tab in enumerate(TABS, 1):
        z.writestr(f"xl/worksheets/sheet{i}.xml", worksheet_xml(tabs[tab], tab == "Sensitivity"))
    z.writestr("xl/worksheets/_rels/sheet7.xml.rels", sheet_drawing_rels)
    z.writestr("xl/drawings/drawing1.xml", drawing_xml())
    z.writestr("xl/drawings/_rels/drawing1.xml.rels", drawing_rels)
    z.writestr("xl/charts/chart1.xml", chart_xml())
    z.writestr("docProps/core.xml",
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">'
        '<dc:title>Scenario 12 EUR Receivable Hedge Model</dc:title><dc:creator>Meghan Hernandez</dc:creator></cp:coreProperties>')
print(f"Built {OUT}; {len(names)} allowed defined names; {len(formulas)} formula cells; all 11 grid rows contain formulas; formula audit passed.")
