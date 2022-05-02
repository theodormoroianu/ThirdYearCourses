/-
  Logica modala in Lean 4 
-/

/-

Definim tipul inductiv al formulelor din logica modala

  φ ::= p | ¬φ | φ → φ | □φ

unde p este o formula atomica, iar ceilalti conectori logici se obtin:

  φ ∧ ψ := ¬(p → ¬q)
  φ ∨ ψ := ¬(¬p ∧ ¬q)

Dualul operatorului □ se noteaza ⋄ si se defineste astfel:

  ⋄φ    := ¬□¬φ

-/

inductive form  where 
  | atom : form 
  | neg : form → form 
  | impl : form → form → form 
  | box : form → form 

notation:40 "¬"p => form.neg p 
infix:50 "→" => form.impl 
notation p "∧" q => ¬(p → ¬q)
notation p "∨" q => ¬(¬p ∧ ¬q)
prefix:80 "□" => form.box 
notation "⋄"p => ¬(□(¬p))

/-
  *Exercitiu*. Sa se scrie o functie care verifica daca o formula contine cel putin un Box.
-/

open form 

def containsBox : form → Bool := fun p =>
  match p with 
  | atom => false 
  | neg q => containsBox q
  | impl q r => (containsBox q) || (containsBox r)
  | □q => true 

/-
  *Exercitiu*. Sa se scrie o functie care returneaza numarul conectorilor dintr-o formula.
Exemplu: connectors (□p → (p → ¬q)) 
returneaza 4
-/

def connectors : form → Nat := fun p => 
  match p with 
  | atom => 0
  | neg q => 1 + connectors q 
  | impl q r => 1 + connectors q + connectors r 
  | □ p => 1 + connectors p 

/-
  Definim contextul ca fiind o multime Γ de formule
-/

def ctx := List form 

inductive List.element {α : Type _} : List α → α → Prop 
| head : element (a :: l) a 
| cons (a b : α) (l : List α) : element l a → element (b :: l) a

notation Γ "∪" p => p :: Γ
notation p "∈" Γ => List.element Γ p 

/-
  Tipul *proof* pentru demonstratii
-/

inductive prf : ctx → form → Prop where 
| ax { Γ } { p } (h : p ∈ Γ) : prf Γ p 
-- | ax { Γ } { p } : ( p ∈ Γ ) → (prf Γ p)
| pl1 { Γ } { p q } : prf Γ (p → (q → p))
| pl2 { Γ } { p q r } : prf Γ ((p → (q → r)) → ((p → q) → (p → r)))
| pl3 { Γ } { p q } : prf Γ (((¬q) → (¬p)) → (p → q))
| mp { Γ } { p q } (hpq : prf Γ (p → q)) (hp : prf Γ p) : prf Γ q
-- | mp { Γ } { p q } : (prf Γ (p → q)) → (prf Γ p) → (prf Γ q)
| k { Γ } { p q } : prf Γ (□(p → q) → (□p → □q))
| t { Γ } { p } : prf Γ (□p → p) 
| s4 { Γ } { p } : prf Γ (□p → □□p) 
| s5 { Γ } { p } : prf Γ (¬(□p) → □(¬(□p)))
| nec { Γ } { p } (h : (prf [] p)) : prf Γ (□p)

notation Γ "⊢" p => prf Γ p 
notation "⊢" p => prf [] p 

open prf 

theorem idd { p : form } : ⊢ p → p := 
  have h₀ := @pl2 [] p (p → p) p 
  have h₁ := pl1 
  have h₂ := mp h₀ h₁ 
  have h₃ := pl1 
  show ⊢ p → p from mp h₂ h₃   

example { p : form } { Γ : ctx } : Γ ⊢ p → p := by 
  apply mp
  case hpq =>
    apply mp
    case hpq => exact @pl2 Γ p (p → p) p
    case hp => exact pl1 
  case hp => exact pl1 

def L : List Nat := [1, 2, 3]
-- 1 :: 2 :: 3 :: []
example : 1 ∈ L := by constructor 
example : 2 ∈ L := by repeat constructor
example : 3 ∈ L := by repeat constructor 
  
-- Γ ∪ {□(φ → ψ), □φ} ⊢ □ψ 
theorem modal_mp { φ ψ : form } { Γ : ctx } : ((Γ ∪ □(φ → ψ)) ∪ □φ) ⊢ □ψ := 
  have h₀ : ((Γ ∪ □(φ → ψ)) ∪ □φ) ⊢ □(φ → ψ) := ax $ by repeat constructor 
  have h₁ : ((Γ ∪ □(φ → ψ)) ∪ □φ) ⊢ □φ := ax $ by repeat constructor 
  have h₂ : ((Γ ∪ □(φ → ψ)) ∪ □φ) ⊢ (□(φ → ψ)) → (□φ → □ψ) := k 
  have h₃ : ((Γ ∪ □(φ → ψ)) ∪ □φ) ⊢ (□φ → □ψ) := mp h₂ h₀ 
  show ((Γ ∪ □(φ → ψ)) ∪ □φ) ⊢ □ψ from mp h₃ h₁ 
  

example { p q : form } : ⊢ □p → □(q → p) := mp k $ nec pl1

example { p q : form } : (⊢ (p → q)) → ⊢ (□p → □q) := 
  fun hpq => mp k (nec hpq)  

example { p q : form } : (⊢ (p → q)) → ⊢ (□p → □q) := 
  fun h₀ : ⊢ (p → q) =>
  have h₁ : ⊢ □(p → q) := nec h₀ 
  have h₂ : ⊢ □(p → q) → (□p → □q) := k 
  show ⊢ □p → □q from mp h₂ h₁ 