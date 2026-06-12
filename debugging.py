from pypdf import PdfReader

reader = PdfReader("standards/DNV_Cybersec.pdf")
print("Pages:", len(reader.pages))
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    print(f"\nPAGE {i+1}")
    print(repr(text[:300] if text else text))
