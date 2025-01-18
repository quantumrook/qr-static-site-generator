reserved_words = {
    r'#+(?P<comment>[ ]*[\S ]*)' : r'<span class="comment">#\g<comment></span>',
    r'(?P<leadingspace>\s*)(?P<name>\S*)\(' : r'\g<leadingspace><span class="method">\g<name></span>(',
    r'^(?P<leadingspace>\s*)[f][o][r]' : r'\g<leadingspace><span class="keyword">for</span>',
    r'(?P<leadingspace>\s)[i][n]' : r'\g<leadingspace><span class="keyword">in</span>'
}