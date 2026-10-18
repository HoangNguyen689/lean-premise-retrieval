# 20 truy vấn kiểm tra (sinh bởi scripts/make_check_queries.py)

Mục đích: kiểm tra bằng mắt định nghĩa truy vấn và premise đúng trong `docs/benchmark_spec.md` trước khi chạy thí nghiệm. 20 truy vấn lấy từ `random/val` (seed 42), mỗi lĩnh vực nhiều nhất 2 truy vấn, bắt buộc có truy vấn nhiều premise đúng và truy vấn bị bỏ bớt premise đúng. Dữ liệu máy đọc: `data_sample/check_queries.jsonl`.

Kiểm tra tự động:

- **C1** mọi premise đúng được đánh dấu `<a>` trong tactic gốc
- **C2** mọi premise đúng truy cập được từ theorem (import hoặc khai báo trước trong cùng file)
- **C3** theorem đang chứng minh không phải premise đúng
- **C4** premise chú thích mà không có trong corpus đều nằm trong `dead_letter.parquet`

| Kiểm tra | C1 | C2 | C3 | C4 |
|---|---|---|---|---|
| Số truy vấn đạt / 20 | 20 | 20 | 20 | 20 |

Có ít nhất một premise đúng trong top-10: B0 1/20, V4 11/20.

Người kiểm tra điền hai dòng cuối mỗi truy vấn. Mọi truy vấn đánh dấu *có vấn đề* phải mở issue và, nếu đổi định nghĩa, nâng phiên bản benchmark spec.

### 1. `random:val:36:0` — Mathlib/Algebra

- Theorem: `mul_invOf_mul_self_cancel` (`Mathlib/Algebra/Group/Invertible/Defs.lean`, dòng 136)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
simp [<a>mul_assoc</a>]
```

- Proof state (truy vấn):

```lean
α : Type u
inst✝¹ : Monoid α
a b : α
inst✝ : Invertible b
⊢ a * ⅟b * b = a
```

- Premise đúng:
  - `mul_assoc` (theorem, `Mathlib/Algebra/Group/Defs.lean`) — hạng B0: >100, V4: >100  
    `theorem mul_assoc : ∀ a b c : G, a * b * c = a * (b * c)`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 2. `random:val:128:5` — Mathlib/NumberTheory

- Theorem: `Fermat42.coprime_of_minimal` (`Mathlib/NumberTheory/FLT/Four.lean`, dòng 89)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
have hpc : (p : ℤ) ^ 2 ∣ c := by
    rw [← <a>Int.pow_dvd_pow_iff</a> <a>two_ne_zero</a>, ← h.1.2.2]
    apply <a>Dvd.intro</a> (a1 ^ 4 + b1 ^ 4)
    ring
```

- Proof state (truy vấn):

```lean
case intro.intro.intro.intro.intro
c : ℤ
p : ℕ
hp : Nat.Prime p
a1 : ℤ
hpa : p ∣ (↑p * a1).natAbs
b1 : ℤ
hpb : p ∣ (↑p * b1).natAbs
h : Minimal (↑p * a1) (↑p * b1) c
hab : ¬(↑p * a1).gcd (↑p * b1) = 1
⊢ False
```

- Premise đúng:
  - `Dvd.intro` (theorem, `Mathlib/Algebra/Divisibility/Basic.lean`) — hạng B0: 58, V4: 15  
    `theorem Dvd.intro (c : α) (h : a * c = b) : a ∣ b`
  - `Int.pow_dvd_pow_iff` (theorem, `Mathlib/Data/Int/GCD.lean`) — hạng B0: >100, V4: >100  
    `theorem pow_dvd_pow_iff {m n : ℤ} {k : ℕ} (k0 : k ≠ 0) : m ^ k ∣ n ^ k ↔ m ∣ n`
  - `two_ne_zero` (lemma, `Mathlib/Algebra/NeZero.lean`) — hạng B0: >100, V4: >100  
    `lemma two_ne_zero [OfNat α 2] [NeZero (2 : α)] : (2 : α) ≠ 0`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 3. `random:val:129:5` — Mathlib/CategoryTheory

- Theorem: `CategoryTheory.OverPresheafAux.counitForward_naturality₂` (`Mathlib/CategoryTheory/Comma/Presheaf.lean`, dòng 507)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
simp [← <a>CostructuredArrow.eq_mk</a>]
```

- Proof state (truy vấn):

```lean
C : Type u
inst✝ : Category.{v, u} C
A : Cᵒᵖ ⥤ Type v
F : (CostructuredArrow yoneda A)ᵒᵖ ⥤ Type v
X : C
s t : (CostructuredArrow yoneda A)ᵒᵖ
f : t ⟶ s
x : F.obj t
⊢ s = { unop := CostructuredArrow.mk (yoneda.map f.unop.left ≫ t.unop.hom) }
```

- Premise đúng:
  - `CategoryTheory.CostructuredArrow.eq_mk` (theorem, `Mathlib/CategoryTheory/Comma/StructuredArrow.lean`) — hạng B0: 79, V4: 31  
    `theorem eq_mk (f : CostructuredArrow S T) : f = mk f.hom`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 4. `random:val:302:2` — Mathlib/Geometry

- Theorem: `PartialHomeomorph.tendsto_extend_comp_iff` (`Mathlib/Geometry/Manifold/SmoothManifoldWithCorners.lean`, dòng 976)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
rw [<a>extend_left_inv</a> _ _ hy] at this
```

- Proof state (truy vấn):

```lean
𝕜 : Type u_1
E : Type u_2
M : Type u_3
H : Type u_4
E' : Type u_5
M' : Type u_6
H' : Type u_7
inst✝⁸ : NontriviallyNormedField 𝕜
inst✝⁷ : NormedAddCommGroup E
inst✝⁶ : NormedSpace 𝕜 E
inst✝⁵ : TopologicalSpace H
inst✝⁴ : TopologicalSpace M
f f' : PartialHomeomorph M H
I : ModelWithCorners 𝕜 E H
inst✝³ : NormedAddCommGroup E'
inst✝² : NormedSpace 𝕜 E'
inst✝¹ : TopologicalSpace H'
inst✝ : Topologica …
```

- Premise đúng:
  - `PartialHomeomorph.extend_left_inv` (theorem, `Mathlib/Geometry/Manifold/SmoothManifoldWithCorners.lean`) — hạng B0: >100, V4: 9  
    `theorem extend_left_inv {x : M} (hxf : x ∈ f.source) : (f.extend I).symm (f.extend I x) = x`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 5. `random:val:363:5` — Mathlib/CategoryTheory

- Theorem: `Bimod.whisker_exchange_bimod` (`Mathlib/CategoryTheory/Monoidal/Bimod.lean`, dòng 985)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
slice_lhs 1 2 => rw [<a>whisker_exchange</a>]
```

- Proof state (truy vấn):

```lean
case h.h
C : Type u₁
inst✝⁴ : Category.{v₁, u₁} C
inst✝³ : MonoidalCategory C
A B : Mon_ C
M✝ : Bimod A B
inst✝² : HasCoequalizers C
inst✝¹ : (X : C) → PreservesColimitsOfSize.{0, 0, v₁, v₁, u₁, u₁} (tensorLeft X)
inst✝ : (X : C) → PreservesColimitsOfSize.{0, 0, v₁, v₁, u₁, u₁} (tensorRight X)
X Y Z : Mon_ C
M N : Bimod X Y
P Q : Bimod Y Z
f : M ⟶ N
g : P ⟶ Q
⊢ M.X ◁ g.hom ≫
      f.hom ▷ Q.X ≫
   …
```

- Premise đúng:
  - `CategoryTheory.MonoidalCategory.whisker_exchange` (theorem, `Mathlib/CategoryTheory/Monoidal/Category.lean`) — hạng B0: >100, V4: 9  
    `theorem whisker_exchange {W X Y Z : C} (f : W ⟶ X) (g : Y ⟶ Z) : W ◁ g ≫ f ▷ Z = f ▷ Y ≫ X ◁ g`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 6. `random:val:397:2` — Mathlib/GroupTheory

- Theorem: `Equiv.Perm.nodup_toList` (`Mathlib/GroupTheory/Perm/Cycle/Concrete.lean`, dòng 278)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
rw [<a>nodup_iff_nthLe_inj</a>]
```

- Proof state (truy vấn):

```lean
case neg
α : Type u_1
inst✝¹ : Fintype α
inst✝ : DecidableEq α
p✝ : Perm α
x✝ : α
p : Perm α
x : α
hx : ¬p x = x
hc : (p.cycleOf x).IsCycle
⊢ (p.toList x).Nodup
```

- Premise đúng:
  - `List.nodup_iff_nthLe_inj` (theorem, `Mathlib/Data/List/Nodup.lean`) — hạng B0: >100, V4: >100  
    `theorem nodup_iff_nthLe_inj {l : List α} : Nodup l ↔ ∀ i j h₁ h₂, nthLe l i h₁ = nthLe l j h₂ → i = j`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 7. `random:val:550:0` — Mathlib/Topology

- Theorem: `elementalStarAlgebra.starAlgHomClass_ext` (`Mathlib/Topology/Algebra/StarSubalgebra.lean`, dòng 270)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
have : <a>StarAlgHomClass</a> F R (↥(<a>topologicalClosure</a> (<a>adjoin</a> R {a}))) B :=
    <a>inferInstanceAs</a> (<a>StarAlgHomClass</a> F R (<a>elementalStarAlgebra</a> R a) B)
```

- Proof state (truy vấn):

```lean
R : Type u_1
A : Type u_2
B : Type u_3
inst✝¹⁶ : CommSemiring R
inst✝¹⁵ : StarRing R
inst✝¹⁴ : TopologicalSpace A
inst✝¹³ : Semiring A
inst✝¹² : StarRing A
inst✝¹¹ : TopologicalSemiring A
inst✝¹⁰ : ContinuousStar A
inst✝⁹ : Algebra R A
inst✝⁸ : StarModule R A
inst✝⁷ : TopologicalSpace B
inst✝⁶ : Semiring B
inst✝⁵ : StarRing B
inst✝⁴ : Algebra R B
inst✝³ : T2Space B
F : Type u_4
a : A
inst✝² : FunL …
```

- Premise đúng:
  - `StarAlgHomClass` (class, `Mathlib/Algebra/Star/StarAlgHom.lean`) — hạng B0: 22, V4: 24  
    `class StarAlgHomClass (F : Type*) (R A B : outParam Type*) [CommSemiring R] [Semiring A] [Algebra R A] [Star A] [Semiring B] [Algebra R B] [Star B] [FunLike F A …`
  - `StarAlgebra.adjoin` (def, `Mathlib/Algebra/Star/Subalgebra.lean`) — hạng B0: >100, V4: >100  
    `def adjoin (s : Set A) : StarSubalgebra R A`
  - `StarSubalgebra.topologicalClosure` (def, `Mathlib/Topology/Algebra/StarSubalgebra.lean`) — hạng B0: >100, V4: >100  
    `def topologicalClosure (s : StarSubalgebra R A) : StarSubalgebra R A`
  - `elementalStarAlgebra` (def, `Mathlib/Topology/Algebra/StarSubalgebra.lean`) — hạng B0: >100, V4: 2  
    `def elementalStarAlgebra (x : A) : StarSubalgebra R A`
  - `inferInstanceAs` (abbrev, `.lake/packages/lean4/src/lean/Init/Prelude.lean`) — hạng B0: >100, V4: >100  
    `abbrev inferInstanceAs (α : Sort u) [i : α] : α`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 8. `random:val:619:8` — Mathlib/MeasureTheory

- Theorem: `MeasureTheory.exists_upperSemicontinuous_le_integral_le` (`Mathlib/MeasureTheory/Integral/VitaliCaratheodory.lean`, dòng 421)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
exact <a>Filter.eventually_of_forall</a> fun x => by simp [gf x]
```

- Proof state (truy vấn):

```lean
case intro.intro.intro.intro.refine_1
α : Type u_1
inst✝³ : TopologicalSpace α
inst✝² : MeasurableSpace α
inst✝¹ : BorelSpace α
μ : Measure α
inst✝ : μ.WeaklyRegular
f : α → ℝ≥0
fint : Integrable (fun x => ↑(f x)) μ
ε : ℝ≥0
εpos : 0 < ↑ε
If : ∫⁻ (x : α), ↑(f x) ∂μ < ⊤
g : α → ℝ≥0
gf : ∀ (x : α), g x ≤ f x
gcont : UpperSemicontinuous g
gint : ∫⁻ (x : α), ↑(f x) ∂μ ≤ ∫⁻ (x : α), ↑(g x) ∂μ + ↑ε
Ig :  …
```

- Premise đúng:
  - `Filter.eventually_of_forall` (theorem, `Mathlib/Order/Filter/Basic.lean`) — hạng B0: >100, V4: >100  
    `theorem eventually_of_forall {p : α → Prop} {f : Filter α} (hp : ∀ x, p x) : ∀ᶠ x in f, p x`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 9. `random:val:701:0` — Mathlib/Data

- Theorem: `Nat.xor_zero` (`Mathlib/Data/Nat/Bitwise.lean`, dòng 355)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
simp [<a>HXor.hXor</a>, <a>Xor.xor</a>, <a>xor</a>]
```

- Proof state (truy vấn):

```lean
n : ℕ
⊢ n ^^^ 0 = n
```

- Premise đúng:
  - `Nat.xor` (def, `.lake/packages/lean4/src/lean/Init/Data/Nat/Bitwise/Basic.lean`) — hạng B0: >100, V4: >100  
    `def xor : @& Nat → @& Nat → Nat`
- Chú thích nhưng không có trong corpus (đã ghi dead_letter): `HXor.hXor`, `Xor.xor`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 10. `random:val:738:0` — Mathlib/Probability

- Theorem: `ProbabilityTheory.cond_inter_self` (`Mathlib/Probability/ConditionalProbability.lean`, dòng 150)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
rw [<a>cond_apply</a> _ hms, ← <a>Set.inter_assoc</a>, <a>Set.inter_self</a>, ← <a>cond_apply</a> _ hms]
```

- Proof state (truy vấn):

```lean
Ω : Type u_1
Ω' : Type u_2
α : Type u_3
m : MeasurableSpace Ω
m' : MeasurableSpace Ω'
μ : Measure Ω
s t✝ : Set Ω
hms : MeasurableSet s
t : Set Ω
⊢ μ[|s] (s ∩ t) = μ[|s] t
```

- Premise đúng:
  - `ProbabilityTheory.cond_apply` (theorem, `Mathlib/Probability/ConditionalProbability.lean`) — hạng B0: 10, V4: 1  
    `theorem cond_apply (hms : MeasurableSet s) (t : Set Ω) : μ[t|s] = (μ s)⁻¹ * μ (s ∩ t)`
  - `Set.inter_assoc` (theorem, `Mathlib/Data/Set/Basic.lean`) — hạng B0: >100, V4: >100  
    `theorem inter_assoc (a b c : Set α) : a ∩ b ∩ c = a ∩ (b ∩ c)`
  - `Set.inter_self` (theorem, `Mathlib/Data/Set/Basic.lean`) — hạng B0: >100, V4: >100  
    `theorem inter_self (a : Set α) : a ∩ a = a`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 11. `random:val:1057:2` — batteries

- Theorem: `Batteries.RBNode.Path.zoom_del` (`.lake/packages/batteries/Batteries/Data/RBMap/Lemmas.lean`, dòng 711)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
intro | <a>rfl</a>, <a>rfl</a> => rfl
```

- Proof state (truy vấn):

```lean
case h_1
α : Type u_1
cut : α → Ordering
path : Path α
t' : RBNode α
path' : Path α
x✝ : RBNode α
⊢ nil = t' →
    path = path' →
      path.del nil red =
        path'.del t'.delRoot
          (match t' with
          | node c l v r => c
          | x => red)
```

- Premise đúng:
  - `rfl` (def, `.lake/packages/lean4/src/lean/Init/Prelude.lean`) — hạng B0: >100, V4: >100  
    `def rfl {α : Sort u} {a : α} : Eq a a`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 12. `random:val:1140:1` — Mathlib/SetTheory

- Theorem: `Ordinal.principal_opow_omega` (`Mathlib/SetTheory/Ordinal/Principal.lean`, dòng 420)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
apply <a>nat_lt_omega</a>
```

- Proof state (truy vấn):

```lean
a b : Ordinal.{u_1}
m n : ℕ
ha : ↑m < ω
hb : ↑n < ω
⊢ ↑(m ^ n) < ω
```

- Premise đúng:
  - `Ordinal.nat_lt_omega` (theorem, `Mathlib/SetTheory/Ordinal/Arithmetic.lean`) — hạng B0: 71, V4: 1  
    `theorem nat_lt_omega (n : ℕ) : ↑n < ω`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 13. `random:val:1172:5` — Mathlib/RingTheory

- Theorem: `exists_integer_of_is_root_of_monic` (`Mathlib/RingTheory/Polynomial/RationalRoot.lean`, dòng 124)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
have d_ne_zero : <a>algebraMap</a> A K (<a>den</a> A r) ≠ 0 :=
      <a>IsFractionRing.to_map_ne_zero_of_mem_nonZeroDivisors</a> (<a>den</a> A r).<a>prop</a>
```

- Proof state (truy vấn):

```lean
case left
A : Type u_1
K : Type u_2
inst✝⁵ : CommRing A
inst✝⁴ : IsDomain A
inst✝³ : UniqueFactorizationMonoid A
inst✝² : Field K
inst✝¹ : Algebra A K
inst✝ : IsFractionRing A K
p : A[X]
hp : p.Monic
r : K
hr : (aeval r) p = 0
inv : A
h_inv : 1 = ↑(den A r) * inv
⊢ r = (algebraMap A K) (num A r * inv)
```

- Premise đúng:
  - `IsFractionRing.den` (def, `Mathlib/RingTheory/Localization/NumDen.lean`) — hạng B0: >100, V4: 58  
    `noncomputable def den (x : K) : nonZeroDivisors A`
  - `IsFractionRing.to_map_ne_zero_of_mem_nonZeroDivisors` (theorem, `Mathlib/RingTheory/Localization/FractionRing.lean`) — hạng B0: >100, V4: >100  
    `protected theorem to_map_ne_zero_of_mem_nonZeroDivisors [Nontrivial R] {x : R} (hx : x ∈ nonZeroDivisors R) : algebraMap R K x ≠ 0`
  - `Subtype.prop` (theorem, `Mathlib/Data/Subtype.lean`) — hạng B0: >100, V4: >100  
    `theorem prop (x : Subtype p) : p x`
  - `algebraMap` (def, `Mathlib/Algebra/Algebra/Defs.lean`) — hạng B0: >100, V4: 1  
    `def algebraMap (R : Type u) (A : Type v) [CommSemiring R] [Semiring A] [Algebra R A] : R →+* A`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 14. `random:val:1228:0` — Mathlib/RingTheory

- Theorem: `WittVector.ghostFun_natCast` (`Mathlib/RingTheory/WittVector/Basic.lean`, dòng 196)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
induction i <;>
      simp [*, <a>Nat.unaryCast</a>, <a>ghostFun_zero</a>, <a>ghostFun_one</a>, <a>ghostFun_add</a>, -<a>Pi.natCast_def</a>]
```

- Proof state (truy vấn):

```lean
p : ℕ
R : Type u_1
S : Type u_2
T : Type u_3
hp : Fact (Nat.Prime p)
inst✝² : CommRing R
inst✝¹ : CommRing S
inst✝ : CommRing T
α : Type u_4
β : Type u_5
x y : 𝕎 R
i : ℕ
⊢ WittVector.ghostFun i.unaryCast = ↑i
```

- Premise đúng:
  - `Nat.unaryCast` (def, `Mathlib/Data/Nat/Cast/Defs.lean`) — hạng B0: >100, V4: 22  
    `protected def Nat.unaryCast [One R] [Zero R] [Add R] : ℕ → R`
  - `Pi.natCast_def` (theorem, `Mathlib/Data/Nat/Cast/Basic.lean`) — hạng B0: >100, V4: >100  
    `theorem natCast_def (n : ℕ) : (n : ∀ a, π a) = fun _ ↦ ↑n`
- Chú thích nhưng không có trong corpus (đã ghi dead_letter): `_private.Mathlib.RingTheory.WittVector.Basic.0.WittVector.ghostFun_zero`, `_private.Mathlib.RingTheory.WittVector.Basic.0.WittVector.ghostFun_one`, `_private.Mathlib.RingTheory.WittVector.Basic.0.WittVector.ghostFun_add`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 15. `random:val:1502:0` — Mathlib/Algebra

- Theorem: `CategoryTheory.ShortComplex.LeftHomologyMapData.quasiIso_iff` (`Mathlib/Algebra/Homology/ShortComplex/QuasiIso.lean`, dòng 97)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
rw [<a>ShortComplex.quasiIso_iff</a>, γ.homologyMap_eq]
```

- Proof state (truy vấn):

```lean
C : Type u_2
inst✝⁵ : Category.{u_1, u_2} C
inst✝⁴ : HasZeroMorphisms C
S₁ S₂ S₃ S₄ : ShortComplex C
inst✝³ : S₁.HasHomology
inst✝² : S₂.HasHomology
inst✝¹ : S₃.HasHomology
inst✝ : S₄.HasHomology
φ : S₁ ⟶ S₂
h₁ : S₁.LeftHomologyData
h₂ : S₂.LeftHomologyData
γ : LeftHomologyMapData φ h₁ h₂
⊢ QuasiIso φ ↔ IsIso γ.φH
```

- Premise đúng:
  - `CategoryTheory.ShortComplex.quasiIso_iff` (lemma, `Mathlib/Algebra/Homology/ShortComplex/QuasiIso.lean`) — hạng B0: >100, V4: 2  
    `lemma quasiIso_iff (φ : S₁ ⟶ S₂) : QuasiIso φ ↔ IsIso (homologyMap φ)`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 16. `random:val:1588:0` — batteries

- Theorem: `List.isSubperm_iff` (`.lake/packages/batteries/Batteries/Data/List/Perm.lean`, dòng 575)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
simp [<a>isSubperm</a>, <a>subperm_ext_iff</a>]
```

- Proof state (truy vấn):

```lean
α : Type u_1
inst✝ : DecidableEq α
l₁ l₂ : List α
⊢ l₁.isSubperm l₂ = true ↔ l₁ <+~ l₂
```

- Premise đúng:
  - `List.isSubperm` (def, `.lake/packages/batteries/Batteries/Data/List/Basic.lean`) — hạng B0: 14, V4: 7  
    `def isSubperm [BEq α] (l₁ l₂ : List α) : Bool`
  - `List.subperm_ext_iff` (theorem, `.lake/packages/batteries/Batteries/Data/List/Perm.lean`) — hạng B0: 100, V4: 12  
    `theorem subperm_ext_iff {l₁ l₂ : List α} : l₁ <+~ l₂ ↔ ∀ x ∈ l₁, count x l₁ ≤ count x l₂`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 17. `random:val:1682:0` — Mathlib/NumberTheory

- Theorem: `padicNorm.int_eq_one_iff` (`Mathlib/NumberTheory/Padics/PadicNorm.lean`, dòng 268)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
nth_rw 2 [← <a>pow_one</a> p]
```

- Proof state (truy vấn):

```lean
p : ℕ
hp : Fact (Nat.Prime p)
m : ℤ
⊢ padicNorm p ↑m = 1 ↔ ¬↑p ∣ m
```

- Premise đúng:
  - `pow_one` (lemma, `Mathlib/Algebra/Group/Defs.lean`) — hạng B0: >100, V4: >100  
    `lemma pow_one (a : M) : a ^ 1 = a`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 18. `random:val:1725:9` — Mathlib/MeasureTheory

- Theorem: `MeasureTheory.setLIntegral_tilted'` (`Mathlib/MeasureTheory/Measure/Tilted.lean`, dòng 144)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
simp only [hf, <a>not_false_eq_true</a>, <a>tilted_of_not_aemeasurable</a>, <a>Measure.restrict_zero</a>,
      <a>lintegral_zero_measure</a>]
```

- Proof state (truy vấn):

```lean
case neg
α : Type u_1
mα : MeasurableSpace α
μ : Measure α
f✝ f : α → ℝ
g : α → ℝ≥0∞
s : Set α
hs : MeasurableSet s
hf : ¬AEMeasurable f μ
hf' : ¬Integrable (fun x => rexp (f x)) μ
⊢ ∫⁻ (x : α) in s, g x ∂μ.tilted f = ∫⁻ (x : α) in s, ENNReal.ofReal (rexp (f x) / ∫ (x : α), rexp (f x) ∂μ) * g x ∂μ
```

- Premise đúng:
  - `MeasureTheory.Measure.restrict_zero` (theorem, `Mathlib/MeasureTheory/Measure/Restrict.lean`) — hạng B0: >100, V4: >100  
    `theorem restrict_zero {_m0 : MeasurableSpace α} (s : Set α) : (0 : Measure α).restrict s = 0`
  - `MeasureTheory.lintegral_zero_measure` (theorem, `Mathlib/MeasureTheory/Integral/Lebesgue.lean`) — hạng B0: >100, V4: >100  
    `theorem lintegral_zero_measure {m : MeasurableSpace α} (f : α → ℝ≥0∞) : ∫⁻ a, f a ∂(0 : Measure α) = 0`
  - `MeasureTheory.tilted_of_not_aemeasurable` (lemma, `Mathlib/MeasureTheory/Measure/Tilted.lean`) — hạng B0: >100, V4: 8  
    `lemma tilted_of_not_aemeasurable (hf : ¬ AEMeasurable f μ) : μ.tilted f = 0`
  - `not_false_eq_true` (theorem, `.lake/packages/lean4/src/lean/Init/SimpLemmas.lean`) — hạng B0: >100, V4: >100  
    `theorem not_false_eq_true : (¬ False) = True`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 19. `random:val:1762:7` — Mathlib/GroupTheory

- Theorem: `nilpotent_iff_lowerCentralSeries` (`Mathlib/GroupTheory/Nilpotent.lean`, dòng 342)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
exact ⟨n, <a>lowerCentralSeries</a> G, <a>lowerCentralSeries_isDescendingCentralSeries</a>, hn⟩
```

- Proof state (truy vấn):

```lean
case mpr.intro
G : Type u_1
inst✝¹ : Group G
H : Subgroup G
inst✝ : H.Normal
n : ℕ
hn : lowerCentralSeries G n = ⊥
⊢ ∃ n H, IsDescendingCentralSeries H ∧ H n = ⊥
```

- Premise đúng:
  - `lowerCentralSeries` (def, `Mathlib/GroupTheory/Nilpotent.lean`) — hạng B0: 70, V4: 2  
    `def lowerCentralSeries (G : Type*) [Group G] : ℕ → Subgroup G`
  - `lowerCentralSeries_isDescendingCentralSeries` (theorem, `Mathlib/GroupTheory/Nilpotent.lean`) — hạng B0: >100, V4: 4  
    `theorem lowerCentralSeries_isDescendingCentralSeries : IsDescendingCentralSeries (lowerCentralSeries G)`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______

### 20. `random:val:1913:7` — Mathlib/Data

- Theorem: `Real.Wallis.W_eq_factorial_ratio` (`Mathlib/Data/Real/Pi/Wallis.lean`, dòng 62)
- Tactic gốc (chỉ để kiểm tra, không đưa vào truy vấn):

```lean
simp_rw [<a>Nat.mul_succ</a>, <a>Nat.factorial_succ</a>, <a>pow_succ</a>]
```

- Proof state (truy vấn):

```lean
case succ.refine_3
n : ℕ
IH :
  ∏ i ∈ range n, (2 * ↑i + 2) / (2 * ↑i + 1) * ((2 * ↑i + 2) / (2 * ↑i + 3)) =
    2 ^ (4 * n) * ↑n ! ^ 4 / (↑(2 * n)! ^ 2 * (2 * ↑n + 1))
⊢ 2 ^ (4 * n) * ↑n ! ^ 4 * ((2 * ↑n + 2) * (2 * ↑n + 2)) * (↑(2 * (n + 1))! ^ 2 * (2 * ↑(n + 1) + 1)) =
    2 ^ (4 * (n + 1)) * ↑(n + 1)! ^ 4 * (↑(2 * n)! ^ 2 * (2 * ↑n + 1) * ((2 * ↑n + 1) * (2 * ↑n + 3)))
```

- Premise đúng:
  - `Nat.factorial_succ` (theorem, `Mathlib/Data/Nat/Factorial/Basic.lean`) — hạng B0: >100, V4: 3  
    `theorem factorial_succ (n : ℕ) : (n + 1)! = (n + 1) * n !`
  - `Nat.mul_succ` (theorem, `.lake/packages/lean4/src/lean/Init/Data/Nat/Basic.lean`) — hạng B0: >100, V4: >100  
    `theorem mul_succ (n m : Nat) : n * succ m = n * m + n`
  - `pow_succ` (theorem, `Mathlib/Algebra/Group/Defs.lean`) — hạng B0: >100, V4: 1  
    `theorem pow_succ (a : M) (n : ℕ) : a ^ (n + 1) = a ^ n * a`
- Kiểm tra tự động: C1 ✓ · C2 ✓ · C3 ✓ · C4 ✓
- Người kiểm tra: ______ · Kết luận: ☐ đúng định nghĩa ☐ có vấn đề (ghi rõ): ______
