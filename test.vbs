Function Soma(x as Integer, y as Integer, cond as boolean) as Integer
  
  Dim a as Integer
  a = x + y + c
  
  if cond then
      Print a*2
  end if


  Soma = a

End Function
  
Sub Main()
  
  Dim a as Integer
  Dim b as Integer
  dim cond as Boolean
  dim c as Integer

  c = 2
  cond = True
  a = 3
  b = Soma(a, 4, cond)
  
  Print a
  Print b

End Sub