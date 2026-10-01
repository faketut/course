
Q1\
1. $f(n)=n^300 log n "and" g(n)=n (log n)^300$\
  $f(n)/g(n)&=(n/(log n))^300 & "given" n/(log n)=infinity\
  &=infinity$
2. $f(n)=sum_(i=1)^n log i "and" g(n)=n log n$\
  $f(n)/g(n)&=(sum_(i=1)^n log i)/(n log n)\
  &<((log n) n)/(n log n)=1\
  &>(n log 1+log n)/(n log n)=1/n=0$

3. $f(n)=2^n "and" g(n)=n!$\
  $f(n)/g(n)&=(2^n)/(n!)\
  &<4/n=0\
  &>0$

4. $f(n)=n^(log n) "and" g(n)=(log n)^n$\
 $f(n)/g(n)&=(n^(log n))/(log n)^n\
 &<(n/(log n))^n=infinity\
 &>(n/(log n))^(log n)=infinity$
5. $f(n)=2^n^0.1 "and" g(n)=(log n)^(log n)$\
  $f(n)/g(n)&=(2^n^0.1)/((log n)^(log n))\
  &=(log(2^n^0.1))/(log((log n)^(log n)))\ 
  &=(n^0.1)/(log n log log n)\
  &<n/(log n log log n)=infinity\
  &>(n^0.1)/(log n)^2=infinity$
6. $f(n)=3^n "and" g(n)=3^(2n)$\
 $f(n)/g(n)=0$

Q2\
1. $T(n)=5T(n/3)+n^6$\
$"master theo."$
2. $T(n)=8T(n/2)+n^3$

3. $T(n)=n T(n-1)+1$
$n!-1$\
$T(n)&<=n c_1 (n-1)!-c_1 +1\
&<=c_1 n!-c_1+1$
4. $T(n)=sqrt(n) T(sqrt(n))+n$
$"let" n=2^m, T(2^m)=2^(m/2) T(2^(m/2))+2^m\
T(2^m)/2^m=T(2^(m/2))/2^(m/2)+1 ", let" s(m)=T(2^m)/2^m\
s(m)=s(m/2)+1, s(m)=O(log  m), T(2^m)=c 2^m log m =c n log log n$\
Q3\
