# fix_uuid_fk.py — run from root

import os
import re

files_dir = "src/domain/entities"

for root, dirs, files in os.walk(files_dir):
    for file in files:
        if not file.endswith(".py"):
            continue

        filepath = os.path.join(root, file)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        original = content

        # replace UUID(as_uuid=True) with Integer in mapped_column
        content = re.sub(r"UUID\(as_uuid=True\)", "Integer", content)

        # replace Mapped[uuid.UUID] with Mapped[int]
        content = re.sub(r"Mapped\[uuid\.UUID\]", "Mapped[int]", content)

        # replace Mapped[Optional[uuid.UUID]] with Mapped[Optional[int]]
        content = re.sub(r"Mapped\[Optional\[uuid\.UUID\]\]", "Mapped[Optional[int]]", content)

        # remove uuid import
        content = re.sub(r"^import uuid\n", "", content, flags=re.MULTILINE)

        # remove UUID from postgresql imports
        content = re.sub(r"from sqlalchemy\.dialects\.postgresql import UUID,\s*", 
                        "from sqlalchemy.dialects.postgresql import ", content)
        content = re.sub(r"from sqlalchemy\.dialects\.postgresql import UUID\n", 
                        "", content)
        content = re.sub(r",\s*UUID", "", content)

        # add Integer to sqlalchemy imports if missing
        if "Mapped[int]" in content and "Integer" not in content:
            content = re.sub(
                r"from sqlalchemy import ([^\n]+)",
                r"from sqlalchemy import Integer, \1",
                content,
                count=1
            )

        if content != original:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Fixed: {filepath}")

print("Done!")