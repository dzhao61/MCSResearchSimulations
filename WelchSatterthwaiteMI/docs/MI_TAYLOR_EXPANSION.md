# Second-Order Taylor Expansion of Mutual Information at Independence

This note derives the Taylor expansion used to describe plug-in mutual
information near independence. It also records the preferred presentation
style for Taylor expansions in this project: define the function, expansion
variable, and expansion point first, then calculate the zeroth-, first-, and
second-order terms separately before combining them.

## 1. General Taylor Formula

For a function $f(z)$ expanded around $z=a$, the second-order Taylor
approximation is

$$
f(z)
\approx
\underbrace{f(a)}_{n=0}
+
\underbrace{f'(a)(z-a)}_{n=1:\ \text{first order}}
+
\underbrace{\frac{f''(a)}{2!}(z-a)^2}_{n=2:\ \text{second order}}.
$$

## 2. Define the MI Cell Function

For one table cell $(x,y)$, define

$$
z=\widehat p(x,y)
\qquad\text{and}\qquad
a=\widehat p(x)\widehat p(y).
$$

Here, $z$ is the observed joint probability and $a$ is the probability fitted
under independence. Their difference is

$$
z-a
=
\widehat p(x,y)-\widehat p(x)\widehat p(y)
=
\delta(x,y).
$$

The cell's contribution to plug-in MI is the function

$$
f(z)=z\log\left(\frac{z}{a}\right).
$$

We now calculate each term in its Taylor expansion around $z=a$.

## 3. Zeroth-Order Term

Evaluate the function at the independence probability:

$$
\begin{aligned}
f(a)
&=a\log\left(\frac{a}{a}\right)\\
&=a\log(1)\\
&=0.
\end{aligned}
$$

Therefore,

$$
\boxed{f(a)=0.}
$$

## 4. First-Order Term

Differentiate the cell function:

$$
\begin{aligned}
f'(z)
&=\frac{d}{dz}
\left[z\log\left(\frac{z}{a}\right)\right]\\
&=\log\left(\frac{z}{a}\right)+1.
\end{aligned}
$$

Evaluate the derivative at $z=a$:

$$
f'(a)
=
\log\left(\frac{a}{a}\right)+1
=1.
$$

The first-order Taylor term is therefore

$$
\begin{aligned}
f'(a)(z-a)
&=1\cdot\delta(x,y)\\
&=\boxed{\delta(x,y)}.
\end{aligned}
$$

## 5. Second-Order Term

Differentiate again:

$$
f''(z)
=
\frac{d}{dz}
\left[\log\left(\frac{z}{a}\right)+1\right]
=
\frac{1}{z}.
$$

Evaluating at $z=a$ gives

$$
f''(a)=\frac{1}{a}.
$$

The second-order Taylor term is therefore

$$
\begin{aligned}
\frac{f''(a)}{2!}(z-a)^2
&=\frac{1}{2a}\delta(x,y)^2\\
&=\boxed{
\frac{\delta(x,y)^2}
{2\widehat p(x)\widehat p(y)}
}.
\end{aligned}
$$

## 6. Combine the Three Terms

For one cell,

$$
f(z)
\approx
\underbrace{0}_{n=0}
+
\underbrace{\delta(x,y)}_{n=1}
+
\underbrace{
\frac{\delta(x,y)^2}
{2\widehat p(x)\widehat p(y)}
}_{n=2}.
$$

Summing over all cells gives

$$
\widehat I(X;Y)
\approx
\underbrace{\sum_{x,y}\delta(x,y)}_{n=1}
+
\underbrace{
\frac{1}{2}\sum_{x,y}
\frac{\delta(x,y)^2}
{\widehat p(x)\widehat p(y)}
}_{n=2}.
$$

The first-order term is

$$
\begin{aligned}
\sum_{x,y}\delta(x,y)
&=\sum_{x,y}\widehat p(x,y)
-\sum_{x,y}\widehat p(x)\widehat p(y)\\
&=1-(1)(1)\\
&=0.
\end{aligned}
$$

Consequently, only the second-order term remains:

$$
\boxed{
\widehat I(X;Y)
\approx
\frac{1}{2}\sum_{x,y}
\frac{
\left\{\widehat p(x,y)-\widehat p(x)\widehat p(y)\right\}^2
}{
\widehat p(x)\widehat p(y)
}.
}
$$

At independence, the zeroth-order term is zero because the MI contribution at
the expansion point is zero. The signed first-order departures cancel across
the table. The squared second-order departures do not cancel and therefore
determine the leading sampling behaviour of MI.

## 7. Presentation Convention

Future Taylor derivations in this project should follow the same sequence:

1. State the general Taylor formula and the retained order.
2. Define the function, variable, and expansion point in the problem's own
   notation.
3. Calculate $f(a)$, $f'(a)$, and $f''(a)$ separately.
4. Substitute each result into its corresponding Taylor term.
5. Combine the terms only after each one has been derived.
6. Explain explicitly why any term vanishes or remains.
