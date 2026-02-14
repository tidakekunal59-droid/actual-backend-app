import Mathlib.GroupTheory.Index
import Mathlib.GroupTheory.QuotientGroup

open Subgroup

variable {G : Type*} [Group G]
variable {H K : Subgroup G}
variable {p : ℕ}

/--
Question 1:
If `H` is a normal subgroup of `G` of prime index `p` then
for all `K ≤ G` either
(i) `K ≤ H` or
(ii) `G = HK` and `|K : K ∩ H|=p`
-/
theorem question_1
  (hHnorm : H.Normal)
  (hp : Fact p.Prime)
  (hHidx : H.index = p) :
  K ≤ H ∨ (H ⊔ K = ⊤ ∧ (H ⊓ K).subgroupOf K |>.index = p) := by
  -- Register H.Normal as an instance for class inference
  haveI := hHnorm

  -- We start with the index multiplication formula relative to the subgroup H ⊔ K.
  -- [H ⊔ K : H] * [G : H ⊔ K] = [G : H] = p
  have h_mul : (H ⊔ K).index * (H.subgroupOf (H ⊔ K)).index = H.index :=
    H.index_mul_index le_sup_left

  -- Substitute the given index p
  rw [hHidx] at h_mul

  -- Since p is prime, the factors must be {1, p} or {p, 1}.
  rcases hp.out.eq_one_or_self_of_dvd _ (dvd_of_mul_right_eq _ h_mul.symm) with h_idx_sup | h_idx_sup

  -- Case 1: [G : H ⊔ K] = 1.
  -- Then [H ⊔ K : H] = p.
  {
    rw [h_idx_sup, one_mul] at h_mul
    -- [G : H ⊔ K] = 1 implies H ⊔ K = ⊤ (i.e., G = HK).
    rw [index_eq_one_iff] at h_idx_sup

    right
    constructor
    · exact h_idx_sup

    -- We need to show [K : K ∩ H] = p.
    -- We use the Second Isomorphism Theorem: (K ⊔ H) / H ≃ K / (H ∩ K).
    -- In Lean Mathlib: QuotientGroup.quotientInfEquivSupQuotient H K
    -- Signature: (H ⊔ K) ⧸ H.subgroupOf (H ⊔ K) ≃* K ⧸ (H ⊓ K).subgroupOf K
    -- (Assuming H is normal).
    let iso := QuotientGroup.quotientInfEquivSupQuotient H K

    -- The isomorphism gives equality of cardinalities (indices).
    -- We have card((H ⊔ K) / H) = card(K / (H ∩ K))
    -- So index of H in H ⊔ K equals index of H ∩ K in K.
    rw [index_eq_card]
    rw [← Nat.card_congr iso.toEquiv]

    -- LHS is now card((H ⊔ K) / H), which is (H.subgroupOf (H ⊔ K)).index
    rw [← index_eq_card]

    -- h_mul says (H.subgroupOf (H ⊔ K)).index = p
    rw [h_mul]
  }

  -- Case 2: [G : H ⊔ K] = p.
  -- Then [H ⊔ K : H] = 1.
  {
    rw [h_idx_sup] at h_mul
    -- h_mul is p * index = p.
    -- Since p is prime (p >= 2), p ≠ 0. Cancellation holds.
    have h_sub_one : (H.subgroupOf (H ⊔ K)).index = 1 :=
      mul_left_cancel₀ (ne_of_gt hp.out.one_lt) h_mul

    -- [H ⊔ K : H] = 1 implies H.subgroupOf (H ⊔ K) = ⊤.
    -- This means (H ∩ (H ⊔ K)) relative to H ⊔ K is the whole group H ⊔ K.
    -- More formally: H.subgroupOf (H ⊔ K) = ⊤ means ∀ x ∈ H ⊔ K, x ∈ H.
    have h_le : H ⊔ K ≤ H := by
      rw [index_eq_one_iff] at h_sub_one
      -- H.subgroupOf (H ⊔ K) is the subgroup H relative to (H ⊔ K).
      -- If it's Top, then every element of (H ⊔ K) is in H.
      intro x hx
      have hx_sub : (⟨x, hx⟩ : H ⊔ K) ∈ H.subgroupOf (H ⊔ K) := by
        rw [h_sub_one]
        exact mem_top _
      exact hx_sub

    -- Since K ≤ H ⊔ K, we have K ≤ H.
    left
    exact le_trans le_sup_right h_le
  }
