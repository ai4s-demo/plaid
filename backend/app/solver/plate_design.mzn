% PLAID Plate Layout Optimization - MiniZinc Model
% Constraint programming model for microwell plate layout design.
% Uses Gecode solver (bundled with MiniZinc).

include "globals.mzn";

% ==================== Parameters ====================

% Plate dimensions
int: num_plates;
int: num_rows;
int: num_cols;
int: size_empty_edge;

% Effective inner dimensions
int: inner_row_start = size_empty_edge;
int: inner_row_end = num_rows - size_empty_edge - 1;
int: inner_col_start = size_empty_edge;
int: inner_col_end = num_cols - size_empty_edge - 1;
int: inner_rows = num_rows - 2 * size_empty_edge;
int: inner_cols = num_cols - 2 * size_empty_edge;

% Compounds (genes)
int: num_compounds;
array[1..num_compounds] of int: compound_replicates;

% Controls
int: num_controls;
array[1..num_controls] of int: control_replicates;

% Total experiments = sum of all compound replicates + control replicates
int: num_compound_experiments = sum(compound_replicates);
int: num_control_experiments = sum(control_replicates);
int: num_experiments = num_compound_experiments + num_control_experiments;

% Precomputed mapping: experiment index -> compound/control ID
% For compound experiments: 1..num_compounds
% For control experiments: num_compounds+1..num_compounds+num_controls
array[1..num_experiments] of int: experiment_compound_id;

% Constraint toggles
bool: enable_no_adjacent;
bool: enable_spread_rows;
bool: enable_spread_cols;
bool: enable_quadrant_balance;
bool: enable_row_col_balance;
bool: enable_control_spread;

% Penalty weights for soft constraints
int: weight_quadrant = 10;
int: weight_row_col = 5;
int: weight_control_spread = 3;

% ==================== Decision Variables ====================

% Each experiment is assigned a plate, row, and column
array[1..num_experiments] of var 1..num_plates: experiment_plate;
array[1..num_experiments] of var inner_row_start..inner_row_end: experiment_row;
array[1..num_experiments] of var inner_col_start..inner_col_end: experiment_col;

% Encoded position for uniqueness: plate * (num_rows * num_cols) + row * num_cols + col
array[1..num_experiments] of var int: experiment_position;
constraint forall(e in 1..num_experiments)(
    experiment_position[e] = (experiment_plate[e] - 1) * num_rows * num_cols
                           + experiment_row[e] * num_cols
                           + experiment_col[e]
);

% ==================== Hard Constraints ====================

% 1. Position uniqueness - no two experiments at the same plate+row+col
constraint alldifferent(experiment_position);

% 2. No adjacent same type (8-direction) on the same plate
constraint if enable_no_adjacent then
    forall(e1 in 1..num_experiments, e2 in e1+1..num_experiments
           where experiment_compound_id[e1] = experiment_compound_id[e2])(
        % Same compound pair must not be adjacent on same plate
        experiment_plate[e1] != experiment_plate[e2]
        \/ abs(experiment_row[e1] - experiment_row[e2]) > 1
        \/ abs(experiment_col[e1] - experiment_col[e2]) > 1
    )
endif;

% ==================== Soft Constraints (via penalty minimization) ====================

% 3. Spread replicates across different rows
var int: penalty_spread_rows;
constraint if enable_spread_rows then
    penalty_spread_rows = sum(c in 1..num_compounds where compound_replicates[c] > 1)(
        let {
            set of int: exps_c = {e | e in 1..num_experiments where experiment_compound_id[e] = c};
            int: n_reps = compound_replicates[c];
        } in
        if n_reps <= inner_rows then
            % Count row collisions for this compound
            sum(e1 in exps_c, e2 in exps_c where e1 < e2)(
                bool2int(experiment_plate[e1] = experiment_plate[e2]
                         /\ experiment_row[e1] = experiment_row[e2])
            )
        else 0 endif
    )
else
    penalty_spread_rows = 0
endif;

% 4. Spread replicates across different columns
var int: penalty_spread_cols;
constraint if enable_spread_cols then
    penalty_spread_cols = sum(c in 1..num_compounds where compound_replicates[c] > 1)(
        let {
            set of int: exps_c = {e | e in 1..num_experiments where experiment_compound_id[e] = c};
            int: n_reps = compound_replicates[c];
        } in
        if n_reps <= inner_cols then
            sum(e1 in exps_c, e2 in exps_c where e1 < e2)(
                bool2int(experiment_plate[e1] = experiment_plate[e2]
                         /\ experiment_col[e1] = experiment_col[e2])
            )
        else 0 endif
    )
else
    penalty_spread_cols = 0
endif;

% 5. Quadrant balance: upper/lower and left/right halves per plate
int: mid_row = inner_row_start + inner_rows div 2;
int: mid_col = inner_col_start + inner_cols div 2;

var int: penalty_quadrant;
constraint if enable_quadrant_balance then
    penalty_quadrant = sum(p in 1..num_plates)(
        let {
            var int: upper = sum(e in 1..num_experiments)(
                bool2int(experiment_plate[e] = p /\ experiment_row[e] < mid_row)
            );
            var int: lower = sum(e in 1..num_experiments)(
                bool2int(experiment_plate[e] = p /\ experiment_row[e] >= mid_row)
            );
            var int: left = sum(e in 1..num_experiments)(
                bool2int(experiment_plate[e] = p /\ experiment_col[e] < mid_col)
            );
            var int: right = sum(e in 1..num_experiments)(
                bool2int(experiment_plate[e] = p /\ experiment_col[e] >= mid_col)
            );
        } in abs(upper - lower) + abs(left - right)
    )
else
    penalty_quadrant = 0
endif;

% 6. Row/column count balance per plate
var int: penalty_row_col;
constraint if enable_row_col_balance then
    let {
        int: ideal_per_row = num_experiments div (num_plates * inner_rows);
        int: ideal_per_col = num_experiments div (num_plates * inner_cols);
    } in
    penalty_row_col = sum(p in 1..num_plates)(
        sum(r in inner_row_start..inner_row_end)(
            let {
                var int: cnt = sum(e in 1..num_experiments)(
                    bool2int(experiment_plate[e] = p /\ experiment_row[e] = r)
                );
            } in abs(cnt - ideal_per_row)
        )
        + sum(c in inner_col_start..inner_col_end)(
            let {
                var int: cnt = sum(e in 1..num_experiments)(
                    bool2int(experiment_plate[e] = p /\ experiment_col[e] = c)
                );
            } in abs(cnt - ideal_per_col)
        )
    )
else
    penalty_row_col = 0
endif;

% 7. Control spacing: controls should not be too close to each other
var int: penalty_control_spread;
constraint if enable_control_spread /\ num_control_experiments > 0 then
    penalty_control_spread = sum(
        e1 in num_compound_experiments+1..num_experiments,
        e2 in e1+1..num_experiments)(
        bool2int(
            experiment_plate[e1] = experiment_plate[e2]
            /\ abs(experiment_row[e1] - experiment_row[e2]) <= 1
            /\ abs(experiment_col[e1] - experiment_col[e2]) <= 1
        )
    )
else
    penalty_control_spread = 0
endif;

% ==================== Objective ====================

var int: total_penalty =
    weight_quadrant * penalty_quadrant
    + weight_row_col * penalty_row_col
    + weight_control_spread * penalty_control_spread
    + 20 * penalty_spread_rows
    + 20 * penalty_spread_cols;

solve :: restart_luby(250)
      :: seq_search([
    int_search(experiment_plate, first_fail, indomain_random),
    int_search(experiment_row, dom_w_deg, indomain_random),
    int_search(experiment_col, dom_w_deg, indomain_random),
]) minimize total_penalty;
