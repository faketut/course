#set document(title: "CS370 Assignment 3")
#set page(
  paper: "us-letter",
  margin: (x: 0.85in, y: 0.8in),
  footer: context align(center)[#counter(page).display()],
)
#set text(size: 10pt)
#set par(justify: true, leading: 0.65em, spacing: 0.7em)
#set heading(numbering: none, outlined: false)
#set raw(theme: none)

== 1. (4 marks) Inverse discrete Fourier transform

The DFT convention used in the course is
$
  F_k = 1/N sum_(n=0)^(N-1) f_n W^(-n k),
  quad W = e^(2 pi i/N),
$
so the inverse transform is
$
  f_n = sum_(k=0)^(N-1) F_k W^(n k).
$
Here $N=4$, $W=e^(2 pi i/4)=i$, and
$
  F = (3.5, 2.5+2i, -2.5, 2.5-2i).
$
Using $W^0=1$, $W^1=i$, $W^2=-1$, and $W^3=-i$:

$
  f_0 &= F_0 + F_1 + F_2 + F_3 \
      &= 3.5 + (2.5+2i) + (-2.5) + (2.5-2i) = 6, \
  f_1 &= F_0 + i F_1 - F_2 - i F_3 \
      &= 3.5 + i(2.5+2i) - (-2.5) - i(2.5-2i) = 2, \
  f_2 &= F_0 - F_1 + F_2 - F_3 \
      &= 3.5 - (2.5+2i) + (-2.5) - (2.5-2i) = -4, \
  f_3 &= F_0 - i F_1 - F_2 + i F_3 \
      &= 3.5 - i(2.5+2i) - (-2.5) + i(2.5-2i) = 10.
$

Therefore
$
  f = (6, 2, -4, 10).
$

== 2. (12 marks) Butterfly FFT

The data are
$
  f = (4, 2i, -2i, -4, 4, 2i, -2i, -4).
$

#strong[(a)] The first FFT stage separates even and odd indices:
$
  g &= (f_0, f_2, f_4, f_6) = (4, -2i, 4, -2i), \
  h &= (f_1, f_3, f_5, f_7) = (2i, -4, 2i, -4).
$

#strong[(b)] For four values, the normalized DFT is
$
  G_k = 1/4 sum_(n=0)^3 g_n i^(-n k),
  quad H_k = 1/4 sum_(n=0)^3 h_n i^(-n k).
$
With $i^0=1$, $i^(-1)=-i$, $i^(-2)=-1$, $i^(-3)=i$:

$
  G_0 &= 1/4(4-2i+4-2i) = 2-i, \
  G_1 &= 1/4(4+(-2i)(-i)+4(-1)+(-2i)(i)) = 0, \
  G_2 &= 1/4(4+(-2i)(-1)+4(1)+(-2i)(-1)) = 2+i, \
  G_3 &= 0.
$
#pagebreak()
Similarly,
$
  H_0 &= 1/4(2i-4+2i-4) = -2+i, \
  H_1 &= 1/4(2i+(-4)(-i)+2i(-1)+(-4)(i)) = 0, \
  H_2 &= 1/4(2i+4+2i+4) = 2+i, \
  H_3 &= 0.
$
Thus
$
  G = (2-i, 0, 2+i, 0),
  quad
  H = (-2+i, 0, 2+i, 0).
$

#strong[(c)] For $N=8$, the two length-4 transforms are combined as
$
  F_k &= 1/2(G_k + W^k H_k), \
  F_(k+4) &= 1/2(G_k - W^k H_k),
  quad k=0,1,2,3,
$
where $W=e^(2 pi i/8)=e^(i pi/4)$ and $W^2=i$.

$
  k=0: quad &F_0 = 1/2[(2-i)+(-2+i)] = 0, \
  &F_4 = 1/2[(2-i)-(-2+i)] = 2-i, \
  k=1: quad &F_1 = 0, quad F_5 = 0, \
  k=2: quad &F_2 = 1/2[(2+i)+i(2+i)] = 1/2(1+3i), \
  &F_6 = 1/2[(2+i)-i(2+i)] = 1/2(3-i), \
  k=3: quad &F_3 = 0, quad F_7 = 0.
$
Hence
$
  F = (0, 0, 0.5+1.5i, 0, 2-i, 0, 1.5-0.5i, 0).
$

#strong[(d)] To see the full FFT, split the two length-4 arrays once more:
$
  g_e &= (4,4), quad g_o = (-2i,-2i), \
  h_e &= (2i,2i), quad h_o = (-4,-4).
$
The length-2 normalized DFTs are
$
  "DFT"(4,4) &= (4,0), quad "DFT"(-2i,-2i) = (-2i,0), \
  "DFT"(2i,2i) &= (2i,0), quad "DFT"(-4,-4) = (-4,0).
$
Combining these pairs gives the same length-4 transforms:
$
  G_0 &= 1/2(4-2i)=2-i, quad G_2 = 1/2(4+2i)=2+i, quad G_1=G_3=0, \
  H_0 &= 1/2(2i-4)=-2+i, quad H_2 = 1/2(2i+4)=2+i, quad H_1=H_3=0.
$
The final butterfly combination is exactly the one in part (c), so the full FFT produces
$
  F = (0, 0, 0.5+1.5i, 0, 2-i, 0, 1.5-0.5i, 0).
$

#pagebreak()
== 3. (8 marks) Fourier coefficients of simple sequences

Recall
$
  F_k = 1/N sum_(n=0)^(N-1) f_n W^(-n k),
  quad W=e^(2 pi i/N),
$
and
$
  1/N sum_(n=0)^(N-1) W^(m n) =
  cases(1 & m equiv 0 (mod N), 0 & "otherwise".)
$

#strong[(a)] Since
$
  cos(4 pi n/N) = 1/2(e^(4 pi i n/N)+e^(-4 pi i n/N))
  = 1/2(W^(2n)+W^(-2n)),
$
we have
$
  f_n = i cos(4 pi n/N) = i/2(W^(2n)+W^(-2n)).
$
Therefore
$
  F_k = i/2(delta_(k,2)+delta_(k,N-2)).
$
For $N>4$, the two indices are distinct, so
$
  F_2 = i/2, quad F_(N-2) = i/2, quad F_k = 0 "otherwise."
$

#strong[(b)] For
$
  f_n = W^(3n)-2,
$
the transform is
$
  F_k = 1/N sum_(n=0)^(N-1) W^((3-k)n) - 2/N sum_(n=0)^(N-1) W^(-n k).
$
The first sum is $N$ only when $k=3$; the second is $N$ only when $k=0$. Hence
$
  F_k = delta_(k,3) - 2 delta_(k,0).
$
For $N>3$,
$
  F_0=-2, quad F_3=1, quad F_k=0 "otherwise."
$

== 4. (8 marks) Every other coefficient is zero

Let $N$ be even and let
$
  f_n = cases(0 & "for " 0 <= n < N/2, 1 & "for " N/2 <= n < N.)
$
For $k=1,2,...,N/2-1$,
$
  F_(2k) = 1/N sum_(n=N/2)^(N-1) W^(-2k n).
$
Put $n=N/2+m$, where $m=0,1,...,N/2-1$. Then
$
  W^(-2k n)
  = e^(-(2 pi i/N) 2k (N/2+m))
  = e^(-2 pi i k)e^(-4 pi i k m/N)
  = e^(-4 pi i k m/N).
$
Thus
$
  F_(2k) = 1/N sum_(m=0)^(N/2-1) r^m,
  quad r=e^(-4 pi i k/N).
$
For $1 <= k <= N/2-1$, $r != 1$, and
$
  r^(N/2) = e^(-2 pi i k) = 1.
$
The finite geometric sum is therefore
$
  sum_(m=0)^(N/2-1) r^m = (1-r^(N/2))/(1-r)=0.
$
Hence
$
  F_(2k)=0, quad k=1,2,...,N/2-1.
$
This completes the proof.

== 5. (10 marks) Audio signal processing

The notebook `A3Q5.ipynb` loads `train_bird.wav` and computes the DFT. The file has
$
  F_s = 8192 "Hz", quad N=12880, quad N/F_s = 1.5723 "s".
$
The original time signal and the magnitude of its DFT are shown in Figure 1. The spectrum has strong train-whistle components below about 2200 Hz, while the bird chirps occupy the band above roughly 2200 Hz. A cutoff frequency of 2200 Hz is therefore a practical separation point.

#figure(
  image("q5_original.png", width: 100%),
  caption: [Original combined signal and the magnitude of its DFT.],
)

The DFT index corresponding to a frequency $f$ is $k=f N/F_s$. For the chosen cutoff,
$
  p = round(2200 / (F_s/N)) = 3459,
  quad p F_s/N = 2200.01 "Hz".
$
The low-pass mask is
$
  Q_k^("low") = cases(0 & p < k < N-p, 1 & "otherwise,")
$
and the high-pass mask is
$
  Q_k^("high") = cases(0 & k <= p " or " k >= N-p, 1 & "otherwise.")
$
These masks satisfy $Q_k=Q_(N-k)$, so they preserve conjugate symmetry. The filtered frequency data and time signals are
$
  hat(Y)^("low") = Y Q^("low"), quad hat(y)^("low") = "Re"(upright("ifft")(hat(Y)^("low"))),
$
$
  hat(Y)^("high") = Y Q^("high"), quad hat(y)^("high") = "Re"(upright("ifft")(hat(Y)^("high"))).
$
The filter is applied by the following direct DFT masking code, with no library filtering routine:

```python
def lowpass_mask(N, Fs, cutoff):
    p = int(round(cutoff / (Fs / N)))
    Q = np.ones(N)
    Q[p + 1:N - p] = 0.0
    return Q, p

def highpass_mask(N, Fs, cutoff):
    p = int(round(cutoff / (Fs / N)))
    Q = np.ones(N)
    Q[:p + 1] = 0.0
    Q[N - p:] = 0.0
    return Q, p
```

#figure(
  image("q5_filtered.png", width: 100%),
  caption: [Low-pass filtered train signal and high-pass filtered bird signal, in both time and frequency domains.],
)
The train component retains the low-frequency whistle harmonics, and the bird component retains the higher-frequency chirps. The notebook also plays both filtered signals with `IPython.display.Audio`.

== 6. (16 marks) DFT-based image compression

The notebook `A3Q6.ipynb` implements all parts on the $512 times 512$ grayscale image `operahall.png`.

#strong[(a)] The top-left $32 times 32$ block and the magnitude of its 2D DFT are shown in Figure 3. The DFT is not shifted, so the zero-frequency (DC) coefficient is at pixel $(0,0)$. This pixel is the brightest in $|F|$, with
$
  |F_(0,0)| = 519.2353 = sum_(i=0)^(31) sum_(j=0)^(31) f_(i,j).
$
The DC coefficient measures the total (and therefore average) brightness of the block. Zeroing it removes the block's mean brightness and leaves only the AC coefficients that encode edges and texture.

#figure(
  image("q6_block.png", width: 100%),
  caption: [Top-left $32 times 32$ block, linear and log magnitudes of its DFT, and the magnitude after removing the DC coefficient.],
)

#strong[(b)] For each $32 times 32$ block, let
$
  F_(k,l) = sum_(i=0)^(31) sum_(j=0)^(31) f_(i,j) e^(-2 pi i(k i + l j)/32),
$
and let $F_max = max_(k,l)|F_(k,l)|$. The thresholding rule is
$
  hat(F)_(k,l) = cases(F_(k,l) & |F_(k,l)| > F_max dot "tol", 0 & |F_(k,l)| <= F_max dot "tol".)
$
The compressed block is $hat(f)="Re"("ifft2"(hat(F)))$. Globally, the drop ratio is
$
  "drop ratio" = "number of nonzero coefficients dropped" / "total number of originally nonzero coefficients".
$
The function used in the notebook is

```python
def Compress(X, tol):
    X = np.asarray(X, dtype=float)
    H, W = X.shape
    Y = np.zeros_like(X)
    total_nonzero = 0
    dropped_nonzero = 0
    for i in range(0, H, 32):
        for j in range(0, W, 32):
            block = X[i:i+32, j:j+32]
            F = np.fft.fft2(block)
            mag = np.abs(F)
            keep = mag > mag.max() * tol
            total_nonzero += int(np.count_nonzero(mag))
            dropped_nonzero += int(np.count_nonzero((mag > 0) & (~keep)))
            Y[i:i+32, j:j+32] = np.real(np.fft.ifft2(F * keep))
    return Y, dropped_nonzero / total_nonzero
```

#strong[(c)] By trial and error on the tolerance, the four values in Table 1 give drop ratios close to the requested levels.

#align(center)[Table 1: Tolerances and resulting drop ratios.]

#table(
  columns: (1fr, 1fr, 1fr),
  table.header([Target drop ratio], [Tolerance $upright("tol")$], [Actual drop ratio]),
  [0.5], [0.0010], [0.4936],
  [0.8], [0.0040], [0.7997],
  [0.92], [0.0094], [0.9202],
  [0.97], [0.020], [0.9699],
)

#figure(
  image("q6_compressed.png", width: 66%),
  caption: [Reconstructions at the four tolerances. Higher drop ratios show increasing block artifacts.],
)

The least compressed image is the one with $upright("tol")=0.0010$ and drop ratio $0.4936$. Its absolute error $|f-hat(f)|$ is shown in Figure 5; the errors are concentrated near edges and block boundaries, as expected when small high-frequency coefficients are discarded.

#figure(
  image("q6_error.png", width: 48%),
  caption: [Absolute error for the least compressed reconstruction, $upright("tol")=0.0010$. The display is saturated at the 99th percentile so that the smaller errors remain visible.],
)
