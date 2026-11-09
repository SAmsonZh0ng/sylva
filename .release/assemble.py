from pathlib import Path
import hashlib, io, json, sys, zipfile

def assemble(root, release):
    root = Path(root).resolve()
    release = Path(release).resolve()
    manifest = json.loads((release/'verify.json').read_text())
    root.mkdir(parents=True, exist_ok=True)
    for spec in manifest['archives']:
        parts = sorted(release.glob(spec['glob']))
        assert parts, 'Missing release archive parts'
        packed = b''.join(p.read_bytes() for p in parts)
        assert hashlib.sha256(packed).hexdigest() == spec['sha256'], 'Archive checksum failed'
        with zipfile.ZipFile(io.BytesIO(packed)) as archive:
            for name in archive.namelist():
                assert not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe archive path'
            archive.extractall(root)
    expected = {r['path']:r['sha256'] for r in manifest['files']}
    for path in root.rglob('*'):
        if path.is_file() and path.relative_to(root).as_posix() not in expected:
            path.unlink()
    for name, digest in expected.items():
        path = (root/name).resolve()
        assert path.is_relative_to(root), 'Unsafe manifest path'
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest, f'Release checksum failed: {name}'
    print(f"Verified {len(expected)} public files for {manifest['release']}.")

if __name__ == '__main__':
    assemble(sys.argv[1] if len(sys.argv)>1 else 'dist', sys.argv[2] if len(sys.argv)>2 else '.release')
