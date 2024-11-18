Require Import Bool.

Notation "! x" := (negb x) (at level 0).



Goal forall x y : bool,
(x && !y) || (!x && !y) || (!x && y) = !(x && y).
Proof.
destruct x, y.
- now simpl.
- now simpl.
- now simpl.
- now simpl.
Qed.


Goal forall x y z : bool,
!(!x && y && z) && !(x && y && !z) && (x && !y && z) = x&& !y && z.
Proof.
destruct x, y, z.
- now simpl.
- now simpl.
- now simpl.
- now simpl.
- now simpl.
- now simpl.
- now simpl.
- now simpl.
Qed.