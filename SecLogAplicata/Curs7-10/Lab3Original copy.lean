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

inductive form where 
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

def containsBox : form → Bool :=
  fun (f: form) =>
    match f with
    | form.atom => false
    | form.neg f' => containsBox f'
    | form.impl f1 f2 => containsBox f1 || containsBox f2
    | form.box _ => true

/-
  *Exercitiu*. Sa se scrie o functie care returneaza numarul conectorilor dintr-o formula.
Exemplu: connectors (□p → (p → ¬q)) 
returneaza 4
-/

def connectors : form → Nat :=
  fun (f: form) =>
    match f with
    | form.atom => 0
    | form.neg f' => 1 + connectors f'
    | form.impl f1 f2 => connectors f1 + connectors f2
    | form.box f' => 1 + connectors f'

/-
  Definim contextul ca fiind o multime Γ de formule
-/

def ctx := List form 

inductive List.element {α : Type _} : List α → α → Prop 
| head : element (a :: l) a 
| cons (a b : α) (l : List α) : element l a → element (b :: l) a

notation Γ "∪" p => p :: Γ
notation p "∆" Γ => List.element Γ p 

/-
  Tipul *proof* pentru demonstratii
-/

inductive prf : ctx → form → Prop where 
| ax { Γ } { p } (h : p ∆ Γ) : prf Γ p 
| pl1 { Γ } { p q } : prf Γ (p → (q → p))
| pl2 { Γ } { p q r } : prf Γ ((p → (q → r)) → ((p → q) → (p → r)))
| pl3 { Γ } { p q } : prf Γ (((¬q) → (¬p)) → (p → q))
| mp { Γ } { p q } (hpq : prf Γ (p → q)) (hp : prf Γ p) : prf Γ q
| k { Γ } { p q } : prf Γ (□(p → q) → (□p → □q))
| t { Γ } { p } : prf Γ (□p → p) 
| s4 { Γ } { p } : prf Γ (□p → □□p) 
| s5 { Γ } { p } : prf Γ (¬(□p) → □(¬(□p)))
| nec { Γ } { p } (h : (prf [] p)) : prf Γ (□p)

notation Γ "⊢" p => prf Γ p 
notation "⊢" p => prf [] p 

open prf 


theorem my_id { p: form } : ⊢ p → p :=
  have h₀: prf [] (p → (p → p)) := pl1
  have h₀': prf [] (p → ((p → p) → p)) := pl1
  have h₁: prf [] ((p → ((p → p) → p)) → ((p → (p → p)) → (p → p))) := pl2
  have h₂ := mp h₁ h₀'
  have h₃ := mp h₂ h₀
  show ⊢ p → p from h₃

theorem idd { p : form } : ⊢ p → p :=
  have h₀ := @pl1 [] p (p → p)
  have h₁ := @pl2 [] p (p → p) p
  have h₂ := mp h₁ h₀
  have h₃ := @pl1 [] p p
  have h₄ := mp h₂ h₃
  show ⊢ p → p from h₄

example { p : form } { Γ : ctx } : Γ ⊢ p → p := by 
  apply mp
  case hpq =>
    apply mp
    case hpq => exact @pl2 Γ p (p → p) p
    case hp => exact pl1 
  case hp => exact pl1 

#check List.elem

def L : List Nat := [1, 2, 3]
example : 1 ∈ L := by constructor
example : 2 ∈ L := by repeat constructor
example : 3 ∈ L := by repeat constructor
  
#check @ax

theorem modal_mp { φ ψ : form } { Γ : ctx } : ((Γ ∪ □(φ → ψ)) ∪ □φ) ⊢ □ψ :=
  have h₀: prf ((Γ ∪ □(φ → ψ)) ∪ □φ) (□(φ → ψ) → (□φ → □ψ)) := k
  have h₁: prf ((Γ ∪ □(φ → ψ)) ∪ □φ) (□(φ → ψ)) := by repeat constructor
  have h₂ := mp h₀ h₁
  have h₃: prf ((Γ ∪ □(φ → ψ)) ∪ □φ) (□φ) := by repeat constructor
  have h₄:= mp h₂ h₃
  show ((Γ ∪ □(φ → ψ)) ∪ □φ) ⊢ □ψ from h₄

example { p q : form } : ⊢ □p → □(q → p) :=
  have h₀ := @pl1 [] p q
  have h₂: ⊢ (□(p→(q→p))) := nec h₀
  have h₃: prf [] (□(p→(q→p)) → (□p→ □(q→p))) := k
  have h₄: prf [] (□p→ □(q→p)) := mp h₃ h₂
  show prf [] (□p → □(q → p)) from h₄

example { p q : form } : (⊢ (p → q)) → ⊢ (□p → □q) :=
  fun hpq: prf [] (p → q) =>
  have h₀: ⊢ □(p → q) := nec hpq
  have h₁: ⊢ □(p → q) → (□p → □q) := k
  have h₂ := mp h₁ h₀  
  show ⊢ (□p → □q)  from h₂
