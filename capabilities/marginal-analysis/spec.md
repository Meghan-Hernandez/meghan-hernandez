# Marginal analysis method

## Model design
Build a transparent, period-based model that separates assumptions, calculations, and outputs. Inputs should include selling price per unit, variable cost per unit, fixed costs, and expected volume. Keep units and currency consistent, and identify each assumption's source and period.

## Named ranges
Use descriptive workbook-level names for the model inputs and key calculations:

- `Price_Per_Unit`
- `Variable_Cost_Per_Unit`
- `Fixed_Costs`
- `Units`
- `Contribution_Per_Unit`
- `Contribution_Margin_Ratio`
- `Break_Even_Units`
- `Operating_Income`

## Formula logic
- Contribution per unit = price per unit - variable cost per unit.
- Contribution margin ratio = contribution per unit / price per unit.
- Break-even units = fixed costs / contribution per unit; round up to a whole unit for an operational threshold.
- Operating income = (contribution per unit × units) - fixed costs.

Check that price per unit is positive and contribution per unit is greater than zero before interpreting break-even units. Present assumptions separately from outputs and verify formulas against an independently calculated example.
