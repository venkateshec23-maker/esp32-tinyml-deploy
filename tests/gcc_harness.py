"""Host parity harness: compiles generated model C with a real gcc.

Why not upstream CompiledClassifier here: setuptools._distutils on Windows
requires MSVC (absent); this box has TDM-GCC. The harness drives the same
contract — CSV vectors in, predictions out — with an explicit toolchain path
and no global machine configuration. Library code still exposes the
upstream-compatible Wrapper.predict() path for environments with a compiler.
"""

import os
import subprocess

GCC = os.environ.get('ESP32_TINYML_GCC', r'C:\TDM-GCC-64\bin\gcc.exe')

_MAIN = r"""
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "model.h"

int main(void) {{
    char line[4096];
    float features[{max_features}];
    while (fgets(line, sizeof(line), stdin)) {{
        int n = 0;
        for (char *tok = strtok(line, ",\n"); tok && n < {max_features};
                tok = strtok(NULL, ",\n"))
            features[n++] = (float)strtod(tok, NULL);
        if (n == 0) continue;
        {call}
    }}
    return 0;
}}
"""

_CALLS = {
    'predict': 'printf("%d\\n", (int){name}_predict(features, n));',
    'regress': 'printf("%.6f\\n", (double){name}_predict(features, n));',
    'proba': ('{{ float out[{k}] = {{0}}; {name}_predict_proba(features, n, out, {k}); '
              'for (int c = 0; c < {k}; c++) printf(c? ",%.6f" : "%.6f", (double)out[c]); '
              'printf("\\n"); }}'),
}


def compile_and_run(header_code, name, X, kind='predict', n_classes=0, workdir='.'):
    os.makedirs(workdir, exist_ok=True)
    n_features = X.shape[1]
    call = _CALLS[kind].format(name=name, k=n_classes or 1)
    with open(os.path.join(workdir, 'model.h'), 'w') as f:
        f.write(header_code)
    with open(os.path.join(workdir, 'main.c'), 'w') as f:
        f.write(_MAIN.format(max_features=n_features, call=call))
    exe = os.path.abspath(os.path.join(workdir, 'parity.exe'))
    r = subprocess.run(
        [GCC, '-std=c99', '-Wall', '-Wextra', '-Werror', '-O2',
         os.path.join(workdir, 'main.c'), '-o', exe, '-lm'],
        capture_output=True, text=True)
    # -lm harmless if ignored on Windows; -Werror keeps generated code honest
    if r.returncode != 0 and 'unrecognized' in (r.stderr or ''):
        r = subprocess.run(
            [GCC, '-std=c99', '-Wall', '-Wextra', '-Werror', '-O2',
             os.path.join(workdir, 'main.c'), '-o', exe],
            capture_output=True, text=True)
    assert r.returncode == 0, f'gcc failed:\n{r.stderr}'
    stdin = '\n'.join(','.join(f'{v:.8f}' for v in row) for row in X)
    r = subprocess.run([exe], input=stdin, capture_output=True, text=True)
    assert r.returncode == 0, f'model binary failed:\n{r.stderr}'
    return [ln for ln in r.stdout.split('\n') if ln]
