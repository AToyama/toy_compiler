Sub Main()
    dim x as boolean
    x = true
    dim y as boolean
    y = false
    dim result as integer
    result = 1
    if x and y then
      result = 2
    else
      result = 3 'comentario
    end if
    print(result)
End Sub