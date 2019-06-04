function soma(x as integer, y as integer) as integer

  soma = x + y

end function

function subtrac(x as integer, y as integer) as integer

  subtrac = x - y

end function

sub rec(num as integer, bool as boolean)

    if bool and bool then
      
      if num > 0 then

        print(num)
        rec(num-1,a)
      
      end if

    end if

end sub

sub main()
  
  dim x as integer
  dim y as integer
  dim a as boolean

  a = true

  x = 10
  
  rec(x, a)
  print(a)

  y = soma(x,x)

  while y > 0 

      print(y)
      y = subtrac(y,1)

  wend

end sub