while True:
    	print("Enter 'x' for exit.")
	hexdec = input("Enter number in Hexadecimal Format: ")
	if hexdec == 'x':
		break
	else:
		dec = int(hexdec, 16)
		print(hexdec,"in Binary =",bin(dec),"\n")