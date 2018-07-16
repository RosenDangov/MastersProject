yes = {'yes','y', 'ye', ''}
no = {'no','n'}

print "Are you sure you want to clear \"lfd.txt\"? (Y/N)" 

choice = raw_input().lower()
if choice in yes:
	print "\"lfd.txt\" cleared."
	open('lfd.txt', 'w').close()
else:
	print "Okay then."
