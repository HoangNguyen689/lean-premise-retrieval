# Ví dụ xuyên suốt: random:val:36:0

```
α : Type u
inst✝¹ : Monoid α
a b : α
inst✝ : Invertible b
⊢ a * ⅟b * b = a
```

Premise đúng: mul_assoc

Token mặc định: ['α', 'type', 'u', 'inst', '¹', 'monoid', 'α', 'a', 'b', 'α', 'inst', 'invertible', 'b', 'a', '⅟b', 'b', 'a']
Token Lean: ['α', 'type', 'inst', '✝', '¹', 'monoid', 'α', 'α', 'inst', '✝', 'invertible', '⊢', '*', '⅟b', '*', '=']

| Hệ thống | Hạng premise đúng | Top 3 |
|---|---|---|
| B0 | ngoài top 100 | Invertible.congr, invOf_add_invOf, invOf_sub_invOf |
| V2 | ngoài top 100 | Invertible.congr, invOf_add_invOf, invOf_sub_invOf |
| V2a | ngoài top 100 | Invertible, invOf_mul_self_assoc, invOf_mul_self_assoc' |
| V4 | ngoài top 100 | invOf_mul_self_assoc, mul_invOf_self, invOf_mul_self |
| V5 | 2 | invOf_mul_self, mul_assoc, one_mul |
