from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("response_analyze.txt")
print(result.text_content)