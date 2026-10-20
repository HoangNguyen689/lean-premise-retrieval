# 30 failure case của V4 (random_test_all)

Cột *Nhãn thủ công* để trống: hai thành viên gán nhãn độc lập rồi đối chiếu.

## 1. `random:test:329:3`
- Theorem: `Matrix.exp_neg` (Mathlib/Analysis)
- Goal: `⊢ exp 𝕂 (-A) = Ring.inverse (exp 𝕂 A)`
- Premise đúng: `NormedAlgebra` (class, dùng 3 lần trong train-A) — hạng V4: 64
  - `class NormedAlgebra (𝕜 : Type*) (𝕜' : Type*) [NormedField 𝕜] [SeminormedRing 𝕜'] extends   Algebra 𝕜 𝕜'`
- Top-3 V4: `Matrix.linftyOpSemiNormedRing`, `Matrix.linftyOpNormedRing`, `Matrix.linftyOpNormedAlgebra`
- Gợi ý tự động: dinh_nghia_instance,nhieu_premise_dung
- Nhãn thủ công: 

## 2. `random:test:1242:2`
- Theorem: `MeasureTheory.Integrable.add_measure` (Mathlib/MeasureTheory)
- Goal: `⊢ snorm f 1 (μ + ν) < ⊤`
- Premise đúng: `MeasureTheory.snorm_one_add_measure` (theorem, dùng 0 lần trong train-A) — hạng V4: 20
  - `theorem snorm_one_add_measure (f : α → F) (μ ν : Measure α) :     snorm f 1 (μ + ν) = snorm f 1 μ + snorm f 1 ν`
- Top-3 V4: `MeasureTheory.memℒp_one_iff_integrable`, `MeasureTheory.Memℒp`, `MeasureTheory.Memℒp.snorm_mk_lt_top`
- Gợi ý tự động: khac
- Nhãn thủ công: 

## 3. `random:test:1463:1`
- Theorem: `StructureGroupoid.restriction_in_maximalAtlas` (Mathlib/Geometry)
- Goal: `⊢ (e.subtypeRestr hs).symm ≫ₕ e' ∈ G ∧ e'.symm ≫ₕ e.subtypeRestr hs ∈ G`
- Premise đúng: `TopologicalSpace.Opens.chart_eq` (lemma, dùng 1 lần trong train-A) — hạng V4: 11
  - `lemma chart_eq {s : Opens M} (hs : Nonempty s) {e : PartialHomeomorph s H} (he : e ∈ atlas H s) :     ∃ x : s, e = (chartAt H (x : M)).subtypeRestr hs`
- Top-3 V4: `StructureGroupoid.trans_restricted`, `StructureGroupoid.compatible`, `chartAt`
- Gợi ý tự động: khac
- Nhãn thủ công: 

## 4. `random:test:1030:4`
- Theorem: `Finset.geomSum_ofColex_strictMono` (Mathlib/Combinatorics)
- Goal: `⊢ ∑ i ∈ { ofColex := s }.ofColex \ { ofColex := t }.ofColex, n ^ i <     ∑ i ∈ { ofColex := t }.ofColex \ { ofColex := s }.ofColex, n ^ i`
- Premise đúng: `Nat.geomSum_lt` (lemma, dùng 0 lần trong train-A) — hạng V4: 64
  - `lemma Nat.geomSum_lt (hm : 2 ≤ m) (hs : ∀ k ∈ s, k < n) : ∑ k ∈ s, m ^ k < m ^ n`
- Top-3 V4: `Finset.Colex.trans_aux`, `Finset.Colex.toColex_le_toColex`, `Finset.Colex.le_def`
- Gợi ý tự động: khong_trung_tu_vung
- Nhãn thủ công: 

## 5. `random:test:356:1`
- Theorem: `Complex.Gamma_integrand_deriv_integrable_A` (Mathlib/Analysis)
- Goal: `⊢ -(↑(rexp (-x✝)) * ↑x✝ ^ s) = (-fun x => ↑(rexp (-x)) * ↑x ^ (s + 1 - 1)) x✝`
- Premise đúng: `Complex.ofReal_neg` (theorem, dùng 34 lần trong train-A) — hạng V4: >100
  - `theorem ofReal_neg (r : ℝ) : ((-r : ℝ) : ℂ) = -r`
- Top-3 V4: `Complex.Gamma_integrand_interval_integrable`, `Complex.GammaIntegral_convergent`, `Complex.cpow_add`
- Gợi ý tự động: ngoai_top100,premise_tong_quat
- Nhãn thủ công: 

## 6. `random:test:1082:0`
- Theorem: `one_le_pow_mul_abs_eval_div` (Mathlib/Algebra)
- Goal: `⊢ 1 ≤ ↑b ^ f.natDegree * |eval (↑a / ↑b) (Polynomial.map (algebraMap ℤ K) f)|`
- Premise đúng: `Int.cast_ne_zero` (lemma, dùng 4 lần trong train-A) — hạng V4: >100
  - `lemma cast_ne_zero : (n : α) ≠ 0 ↔ n ≠ 0`
- Top-3 V4: `Polynomial.natDegree`, `Polynomial.natDegree_C_mul_le`, `Polynomial.natDegree_mul_C_le`
- Gợi ý tự động: ngoai_top100,khong_trung_tu_vung,nhieu_premise_dung
- Nhãn thủ công: 

## 7. `random:test:1497:5`
- Theorem: `VitaliFamily.ae_tendsto_lintegral_nnnorm_sub_div'_of_integrable` (Mathlib/MeasureTheory)
- Goal: `⊢ ∀ᶠ (x_1 : Set α) in v.filterAt x, (∫⁻ (y : α) in x_1, ↑‖f y - f x‖₊ ∂μ) / μ x_1 ≤ ε`
- Premise đúng: `EMetric.mem_closure_iff` (theorem, dùng 5 lần trong train-A) — hạng V4: >100
  - `theorem mem_closure_iff : x ∈ closure s ↔ ∀ ε > 0, ∃ y ∈ s, edist x y < ε`
- Top-3 V4: `VitaliFamily.ae_tendsto_lintegral_div'`, `MeasureTheory.Measure.finiteSpanningSetsInOpen'`, `VitaliFamily.ae_tendsto_measure_inter_div`
- Gợi ý tự động: ngoai_top100,nhieu_premise_dung,truy_van_dai
- Nhãn thủ công: 

## 8. `random:test:1646:16`
- Theorem: `GeneralizedContinuedFraction.compExactValue_correctness_of_stream_eq_some` (Mathlib/Algebra)
- Goal: `⊢ v = if (IntFractPair.of v).fr = 0 then ↑⌊v⌋ else ↑⌊v⌋ + (IntFractPair.of v).fr`
- Premise đúng: `Int.fract` (def, dùng 15 lần trong train-A) — hạng V4: >100
  - `def fract (a : α) : α`
- Top-3 V4: `GeneralizedContinuedFraction.of`, `GeneralizedContinuedFraction.IntFractPair.stream_zero`, `GeneralizedContinuedFraction.IntFractPair.stream_succ_of_some`
- Gợi ý tự động: ngoai_top100,dinh_nghia_instance,nhieu_premise_dung
- Nhãn thủ công: 

## 9. `random:test:396:9`
- Theorem: `ProbabilityTheory.eq_condKernel_of_measure_eq_compProd` (Mathlib/Probability)
- Goal: `⊢ (Measure.map (Prod.map id f) (ρ.fst ⊗ₘ ρ.condKernel)) s = (ρ.fst ⊗ₘ kernel.map ρ.condKernel f ⋯) s`
- Premise đúng: `MeasureTheory.Measure.map_apply` (theorem, dùng 28 lần trong train-A) — hạng V4: >100
  - `theorem map_apply (hf : Measurable f) {s : Set β} (hs : MeasurableSet s) :     μ.map f s = μ (f ⁻¹' s)`
- Top-3 V4: `ProbabilityTheory.eq_condKernel_of_measure_eq_compProd_real`, `ProbabilityTheory.eq_condKernel_of_measure_eq_compProd'`, `MeasureTheory.Measure.compProd_fst_condKernel`
- Gợi ý tự động: ngoai_top100
- Nhãn thủ công: 

## 10. `random:test:1931:3`
- Theorem: `MeasureTheory.integral_Ioi_of_hasDerivAt_of_tendsto` (Mathlib/MeasureTheory)
- Goal: `⊢ f x - f a = ∫ (x : ℝ) in a..id x, f' x`
- Premise đúng: `le_of_lt` (theorem, dùng 170 lần trong train-A) — hạng V4: >100
  - `theorem le_of_lt : ∀ {a b : α}, a < b → a ≤ b`
- Top-3 V4: `MeasureTheory.tendsto_limUnder_of_hasDerivAt_of_integrableOn_Ioi`, `MeasureTheory.tendsto_zero_of_hasDerivAt_of_integrableOn_Ioi`, `HasDerivAt`
- Gợi ý tự động: ngoai_top100,khong_trung_tu_vung,premise_tong_quat
- Nhãn thủ công: 

## 11. `random:test:1413:4`
- Theorem: `Polynomial.Monic.mul_left_ne_zero` (Mathlib/Algebra)
- Goal: `⊢ ¬p.degree = ⊥`
- Premise đúng: `LT.lt.ne'` (theorem, dùng 155 lần trong train-A) — hạng V4: >100
  - `theorem ne' [Preorder α] {x y : α} (h : x < y) : y ≠ x`
- Top-3 V4: `Polynomial.Monic.degree_map`, `Polynomial.Monic.degree_le_zero_iff_eq_one`, `Polynomial.degree_zero`
- Gợi ý tự động: ngoai_top100,khong_trung_tu_vung,premise_tong_quat
- Nhãn thủ công: 

## 12. `random:test:1375:8`
- Theorem: `Set.Intersecting.exists_card_eq` (Mathlib/Combinatorics)
- Goal: `⊢ ∃ t, s ⊆ t ∧ 2 * t.card = Fintype.card α ∧ (↑t).Intersecting`
- Premise đúng: `ssubset_iff_subset_ne` (theorem, dùng 1 lần trong train-A) — hạng V4: >100
  - `theorem ssubset_iff_subset_ne [IsAntisymm α (· ⊆ ·)] : a ⊂ b ↔ a ⊆ b ∧ a ≠ b`
- Top-3 V4: `Set.Intersecting.card_le`, `Fintype.card`, `Set.Intersecting.is_max_iff_card_eq`
- Gợi ý tự động: ngoai_top100,nhieu_premise_dung
- Nhãn thủ công: 

## 13. `random:test:869:0`
- Theorem: `Associates.factors_subsingleton` (Mathlib/RingTheory)
- Goal: `⊢ a.factors = ⊤`
- Premise đúng: `Subsingleton` (class, dùng 13 lần trong train-A) — hạng V4: >100
  - `class Subsingleton (α : Sort u) : Prop`
- Top-3 V4: `Associates.factors_prod`, `UniqueFactorizationMonoid.factors`, `UniqueFactorizationMonoid.normalizedFactors`
- Gợi ý tự động: ngoai_top100,dinh_nghia_instance,nhieu_premise_dung
- Nhãn thủ công: 

## 14. `random:test:769:11`
- Theorem: `ContDiffOn.comp` (Mathlib/Analysis)
- Goal: `⊢ ContDiffOn 𝕜 n (g ∘ f) s`
- Premise đúng: `Function.comp_apply` (theorem, dùng 340 lần trong train-A) — hạng V4: >100
  - `theorem Function.comp_apply {f : β → δ} {g : α → β} {x : α} : comp f g x = f (g x)`
- Top-3 V4: `ContDiffOn.comp_same_univ`, `ContDiffOn`, `ContDiffOn.comp_continuousLinearMap`
- Gợi ý tự động: ngoai_top100,khong_trung_tu_vung,premise_tong_quat,truy_van_dai
- Nhãn thủ công: 

## 15. `random:test:1670:2`
- Theorem: `integrable_rpow_mul_exp_neg_mul_sq` (Mathlib/Analysis)
- Goal: `⊢ IntegrableOn (fun x => x ^ s * rexp (-b * x ^ 2)) (Iio 0) volume`
- Premise đúng: `MeasureTheory.Measure` (structure, dùng 18 lần trong train-A) — hạng V4: >100
  - `structure Measure (α : Type*) [MeasurableSpace α] extends OuterMeasure α`
- Top-3 V4: `integrableOn_rpow_mul_exp_neg_mul_sq`, `integrableOn_rpow_mul_exp_neg_mul_rpow`, `integrableOn_rpow_mul_exp_neg_rpow`
- Gợi ý tự động: ngoai_top100,khong_trung_tu_vung,dinh_nghia_instance,nhieu_premise_dung
- Nhãn thủ công: 

## 16. `random:test:1232:23`
- Theorem: `exists_setIndependent_isCompl_sSup_atoms` (Mathlib/Order)
- Goal: `⊢ Disjoint x (sSup (s \ {x}))`
- Premise đúng: `Set.diff_subset` (theorem, dùng 28 lần trong train-A) — hạng V4: >100
  - `theorem diff_subset {s t : Set α} : s \ t ⊆ s`
- Top-3 V4: `CompleteLattice.setIndependent_iUnion_of_directed`, `CompleteLattice.SetIndependent`, `IsCompactlyGenerated`
- Gợi ý tự động: ngoai_top100,nhieu_premise_dung
- Nhãn thủ công: 

## 17. `random:test:1330:45`
- Theorem: `Collinear.oangle_sign_of_sameRay_vsub` (Mathlib/Geometry)
- Goal: `⊢ (p₁, p₅, p₂) ∈ s`
- Premise đúng: `Set.mem_univ` (theorem, dùng 97 lần trong train-A) — hạng V4: >100
  - `theorem mem_univ (x : α) : x ∈ @univ α`
- Top-3 V4: `collinear_triple_of_mem_affineSpan_pair`, `EuclideanGeometry.oangle_rotate_sign`, `collinear_insert_insert_insert_of_mem_affineSpan_pair`
- Gợi ý tự động: ngoai_top100,premise_tong_quat,nhieu_premise_dung
- Nhãn thủ công: 

## 18. `random:test:969:5`
- Theorem: `Polynomial.coeff_eq_zero_of_lt_natTrailingDegree` (Mathlib/Algebra)
- Goal: `⊢ ↑n < ↑p.natTrailingDegree`
- Premise đúng: `WithTop.coe_lt_coe` (theorem, dùng 6 lần trong train-A) — hạng V4: >100
  - `theorem coe_lt_coe : (a : WithTop α) < b ↔ a < b`
- Top-3 V4: `Polynomial.natTrailingDegree`, `Polynomial.natDegree`, `Polynomial.trailingDegree_eq_natTrailingDegree`
- Gợi ý tự động: ngoai_top100,khong_trung_tu_vung
- Nhãn thủ công: 

## 19. `random:test:1596:0`
- Theorem: `LinearIndependent.cardinal_mk_le_finrank` (Mathlib/LinearAlgebra)
- Goal: `⊢ #ι ≤ ↑(finrank R M)`
- Premise đúng: `Cardinal.lift_le` (theorem, dùng 11 lần trong train-A) — hạng V4: >100
  - `theorem lift_le {a b : Cardinal.{v}} : lift.{u, v} a ≤ lift.{u, v} b ↔ a ≤ b`
- Top-3 V4: `FiniteDimensional.finrank`, `LinearIndependent.cardinal_le_rank`, `finrank_eq_rank`
- Gợi ý tự động: ngoai_top100,khong_trung_tu_vung
- Nhãn thủ công: 

## 20. `random:test:1497:16`
- Theorem: `VitaliFamily.ae_tendsto_lintegral_nnnorm_sub_div'_of_integrable` (Mathlib/MeasureTheory)
- Goal: `⊢ ∫⁻ (y : α), ↑‖f y - (A.set n).indicator (fun x => c) y‖₊ ∂μ ≠ ⊤`
- Premise đúng: `ne_of_lt` (theorem, dùng 67 lần trong train-A) — hạng V4: >100
  - `theorem ne_of_lt {a b : α} (h : a < b) : a ≠ b`
- Top-3 V4: `MeasureTheory.Measure.finiteSpanningSetsInOpen'`, `MeasureTheory.integral_indicator`, `VitaliFamily.ae_tendsto_lintegral_div'`
- Gợi ý tự động: ngoai_top100,premise_tong_quat
- Nhãn thủ công: 

## 21. `random:test:163:24`
- Theorem: `TopologicalSpace.NoetherianSpace.exists_open_ne_empty_le_irreducibleComponent` (Mathlib/Topology)
- Goal: `⊢ a ∈ ⋃₀ insert U ι`
- Premise đúng: `Decidable.not_and_iff_or_not_not` (theorem, dùng 0 lần trong train-A) — hạng V4: >100
  - `theorem Decidable.not_and_iff_or_not_not [Decidable a] : ¬(a ∧ b) ↔ ¬a ∨ ¬b`
- Top-3 V4: `TopologicalSpace.NoetherianSpace.finite_irreducibleComponents`, `TopologicalSpace.NoetherianSpace.exists_finite_set_isClosed_irreducible`, `TopologicalSpace.NoetherianSpace.exists_finite_set_closeds_irreducible`
- Gợi ý tự động: ngoai_top100,khong_trung_tu_vung,nhieu_premise_dung
- Nhãn thủ công: 

## 22. `random:test:892:1`
- Theorem: `AkraBazziRecurrence.GrowsPolynomially.eventually_atTop_nonneg_or_nonpos` (Mathlib/Computability)
- Goal: `⊢ (∀ᶠ (x : ℝ) in atTop, 0 ≤ f x) ∨ ∀ᶠ (x : ℝ) in atTop, f x ≤ 0`
- Premise đúng: `Set.nonempty_of_mem` (theorem, dùng 4 lần trong train-A) — hạng V4: >100
  - `theorem nonempty_of_mem {x} (h : x ∈ s) : s.Nonempty`
- Top-3 V4: `AkraBazziRecurrence.GrowsPolynomially.eventually_atTop_ge`, `AkraBazziRecurrence.GrowsPolynomially.eventually_atTop_le`, `AkraBazziRecurrence.GrowsPolynomially`
- Gợi ý tự động: ngoai_top100,nhieu_premise_dung
- Nhãn thủ công: 

## 23. `random:test:738:3`
- Theorem: `monic_descPochhammer` (Mathlib/RingTheory)
- Goal: `⊢ (descPochhammer R (n + 1)).Monic`
- Premise đúng: `Polynomial.natDegree_X_sub_C` (theorem, dùng 6 lần trong train-A) — hạng V4: >100
  - `theorem natDegree_X_sub_C (x : R) : (X - C x).natDegree = 1`
- Top-3 V4: `descPochhammer_succ_left`, `Polynomial.leadingCoeff`, `descPochhammer_zero`
- Gợi ý tự động: ngoai_top100,khong_trung_tu_vung,nhieu_premise_dung
- Nhãn thủ công: 

## 24. `random:test:163:4`
- Theorem: `TopologicalSpace.NoetherianSpace.exists_open_ne_empty_le_irreducibleComponent` (Mathlib/Topology)
- Goal: `⊢ ∃ o, IsOpen o ∧ o ≠ ∅ ∧ o ≤ Z`
- Premise đúng: `le_antisymm` (theorem, dùng 405 lần trong train-A) — hạng V4: >100
  - `theorem le_antisymm : ∀ {a b : α}, a ≤ b → b ≤ a → a = b`
- Top-3 V4: `TopologicalSpace.NoetherianSpace.finite_irreducibleComponents`, `TopologicalSpace.NoetherianSpace.exists_finite_set_closeds_irreducible`, `TopologicalSpace.NoetherianSpace.exists_finite_set_isClosed_irreducible`
- Gợi ý tự động: ngoai_top100,premise_tong_quat,nhieu_premise_dung
- Nhãn thủ công: 

## 25. `random:test:1821:4`
- Theorem: `Matrix.PosSemidef.fromBlocks₁₁` (Mathlib/LinearAlgebra)
- Goal: `⊢ 0 ≤ star x ⬝ᵥ (D - Bᴴ * A⁻¹ * B) *ᵥ x`
- Premise đúng: `Matrix.dotProduct_mulVec` (theorem, dùng 5 lần trong train-A) — hạng V4: >100
  - `theorem dotProduct_mulVec [Fintype n] [Fintype m] [NonUnitalSemiring R] (v : m → R)     (A : Matrix m n R) (w : n → R) : v ⬝ᵥ A *ᵥ w = v ᵥ* A ⬝ᵥ w`
- Top-3 V4: `Matrix.IsHermitian.fromBlocks₁₁`, `Matrix.IsHermitian.fromBlocks₂₂`, `Matrix.fromBlocks₁₁Invertible`
- Gợi ý tự động: ngoai_top100,nhieu_premise_dung
- Nhãn thủ công: 

## 26. `random:test:220:13`
- Theorem: `AkraBazziRecurrence.GrowsPolynomially.of_isTheta` (Mathlib/Computability)
- Goal: `⊢ ∀ᶠ (x : ℝ) in atTop, ∀ u ∈ Set.Icc (b * x) x, f u ∈ Set.Icc (c₁ * c₂⁻¹ * c₃ * f x) (c₂ * c₄ * c₁⁻¹ * f x)`
- Premise đúng: `inv_mul_cancel` (theorem, dùng 68 lần trong train-A) — hạng V4: >100
  - `theorem inv_mul_cancel (h : a ≠ 0) : a⁻¹ * a = 1`
- Top-3 V4: `AkraBazziRecurrence.GrowsPolynomially.eventually_atTop_ge`, `AkraBazziRecurrence.GrowsPolynomially.eventually_atTop_le`, `AkraBazziRecurrence.GrowsPolynomially.eventually_atTop_ge_nat`
- Gợi ý tự động: ngoai_top100,khong_trung_tu_vung,premise_tong_quat,truy_van_dai
- Nhãn thủ công: 

## 27. `random:test:1330:2`
- Theorem: `Collinear.oangle_sign_of_sameRay_vsub` (Mathlib/Geometry)
- Goal: `⊢ (∡ p₁ p₅ p₂).sign = (∡ p₃ p₅ p₄).sign`
- Premise đúng: `Collinear` (def, dùng 0 lần trong train-A) — hạng V4: >100
  - `def Collinear (s : Set P) : Prop`
- Top-3 V4: `EuclideanGeometry.oangle_rotate_sign`, `EuclideanGeometry.oangle_eq_angle_of_sign_eq_one`, `EuclideanGeometry.angle_eq_iff_oangle_eq_of_sign_eq`
- Gợi ý tự động: ngoai_top100,dinh_nghia_instance,nhieu_premise_dung
- Nhãn thủ công: 

## 28. `random:test:994:0`
- Theorem: `Nat.floor_eq_iff` (Mathlib/Algebra)
- Goal: `⊢ ⌊a⌋₊ = n ↔ ↑n ≤ a ∧ a < ↑n + 1`
- Premise đúng: `Nat.cast_add` (theorem, dùng 84 lần trong train-A) — hạng V4: >100
  - `theorem cast_add [AddMonoidWithOne R] (m n : ℕ) : ((m + n : ℕ) : R) = m + n`
- Top-3 V4: `Nat.floor_lt`, `Nat.floor_le`, `Nat.lt_floor_add_one`
- Gợi ý tự động: ngoai_top100,premise_tong_quat,nhieu_premise_dung
- Nhãn thủ công: 

## 29. `random:test:981:1`
- Theorem: `Zspan.repr_ceil_apply` (Mathlib/Algebra)
- Goal: `⊢ (b.repr ↑(ceil b m)) i = ↑⌈(b.repr m) i⌉`
- Premise đúng: `mul_one` (theorem, dùng 576 lần trong train-A) — hạng V4: >100
  - `theorem mul_one : ∀ a : M, a * 1 = a`
- Top-3 V4: `Int.ceil_intCast`, `Nat.le_ceil`, `Zspan.repr_floor_apply`
- Gợi ý tự động: ngoai_top100,khong_trung_tu_vung,premise_tong_quat,nhieu_premise_dung
- Nhãn thủ công: 

## 30. `random:test:765:4`
- Theorem: `C_p_pow_dvd_bind₁_rename_wittPolynomial_sub_sum` (Mathlib/RingTheory)
- Goal: `⊢ C ↑(p ^ (n + 1)) ∣     (bind₁ fun b => (rename fun i => (b, i)) (W_ ℤ (n + 1))) Φ -       ∑ i ∈ Finset.range (n + 1), C (↑p ^ i) * wittStructureInt p Φ i ^ p ^ (n + 1 - i)`
- Premise đúng: `MvPolynomial.map_bind₁` (theorem, dùng 3 lần trong train-A) — hạng V4: 18
  - `theorem map_bind₁ (f : R →+* S) (g : σ → MvPolynomial τ R) (φ : MvPolynomial σ R) :     map f (bind₁ g φ) = bind₁ (fun i : σ => (map f) (g i)) (map f φ)`
- Top-3 V4: `bind₁_rename_expand_wittPolynomial`, `wittStructureRat`, `wittStructureRat_prop`
- Gợi ý tự động: nhieu_premise_dung
- Nhãn thủ công: 
