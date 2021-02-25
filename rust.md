## [Tutorial](https://www.youtube.com/c/TensorProgramming/search?query=rust)
[Trait std::ops::Index](https://doc.rust-lang.org/std/ops/trait.Index.html)
```rust
fn main() {
    let a = String::from("hello");
    let b = &a[..];
    let c = b[..];
}
// error[E0277]: the size for values of type `str` cannot be known at compilation time
```
> container[index] => *container.index(index)

1. The variable c is str type which cannot be known at compilation time (DST type).
2. The variable b is &str type so we can trace what's going on.
```rust
// https://doc.rust-lang.org/src/core/str/traits.rs.html#56-66
#[stable(feature = "rust1", since = "1.0.0")]
impl<I> ops::Index<I> for str
where
    I: SliceIndex<str>,
{
    type Output = I::Output;

    #[inline]
    fn index(&self, index: I) -> &I::Output {
        index.index(self)
    }
}
```
```rust
#[stable(feature = "str_checked_slicing", since = "1.20.0")]
unsafe impl SliceIndex<str> for ops::RangeFull {
    type Output = str;
    #[inline]
    fn index(self, slice: &str) -> &Self::Output {
        slice
    }
```
Now I fully understand below code.
```rust
fn main() {
    let my_string = String::from("hello world");

    // first_word works on slices of `String`s
    let word = first_word(&my_string[..]);

    let my_string_literal = "hello world";

    // first_word works on slices of string literals
    let word = first_word(&my_string_literal[..]);

    // Because string literals *are* string slices already,
    // this works too, without the slice syntax!
    let word = first_word(my_string_literal);
}
```
