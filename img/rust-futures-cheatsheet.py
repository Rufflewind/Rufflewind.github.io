#!/usr/bin/env python3
s = """
// Constructing leaf futures
fn empty ()             -> Future<T, E>
fn ok    (T)            -> Future<T, E>
fn err   (E)            -> Future<T, E>
fn result(Result<T, E>) -> Future<T, E>

// General future constructor
fn poll_fn(FnMut(thread_local!(Task)) -> Poll<T, E>) -> Future<T, E>

// Mapping futures
fn Future::map     (Future<T, E>, FnOnce(T) -> U) -> Future<U, E>
fn Future::map_err (Future<T, E>, FnOnce(E) -> F) -> Future<T, F>
fn Future::from_err(Future<T, Into<E>>)           -> Future<T, E>

// Chaining (sequencing) futures
fn Future::then    (Future<T, E>, FnOnce(Result<T, E>) -> IntoFuture<U, F>) -> Future<U, F>
fn Future::and_then(Future<T, E>, FnOnce(T)            -> IntoFuture<U, E>) -> Future<U, E>
fn Future::or_else (Future<T, E>, FnOnce(E)            -> IntoFuture<T, F>) -> Future<T, F>
fn Future::flatten (Future<Future<T, E>, Into<E>>)                          -> Future<T, E>

// Joining (waiting) futures
fn Future::join (Future<T, E>, IntoFuture<U, E>)                                                       -> Future<(T, U),          E>
fn Future::join3(Future<T, E>, IntoFuture<U, E>, IntoFuture<V, E>)                                     -> Future<(T, U, V),       E>
fn Future::join4(Future<T, E>, IntoFuture<U, E>, IntoFuture<V, E>, IntoFuture<W, E>)                   -> Future<(T, U, V, W),    E>
fn Future::join5(Future<T, E>, IntoFuture<U, E>, IntoFuture<V, E>, IntoFuture<W, E>, IntoFuture<X, E>) -> Future<(T, U, V, W, X), E>
fn join_all     (IntoIterator<IntoFuture<T, E>>)                                                       -> Future<Vec<T>,          E>

// Selecting (racing) futures
fn Future::select (Future<T, E>, IntoFuture<T, E>) -> Future<(T, Future<T, E>), (E, Future<T, E>)>
fn Future::select2(Future<T, E>, IntoFuture<U, F>) -> Future<Either<(T, Future<U, F>), (U, Future<T, E>)>, Either<(E, Future<U, F>), (F, Future<T, E>)>>
fn select_all     (IntoIterator<IntoFuture<T, E>>) -> Future<(T, usize, Vec<Future<T, E>>), (E, usize, Vec<Future<T, E>>)>
fn select_ok      (IntoIterator<IntoFuture<T, E>>) -> Future<(T, Vec<Future<T, E>>), E>

// Utility
fn lazy         (FnOnce() -> IntoFuture<T, E>)             -> Future<T, E>
fn loop_fn      (S, FnMut(S) -> IntoFuture<Loop<T, S>, E>) -> Future<T, E>
fn Future::boxed(Future<T, E>+Send+'static)                -> Future<T, E>+Send+'static

// Miscellaneous
fn Future::into_stream   (Future<T, E>)            -> Stream<T, E>
fn Future::flatten_stream(Future<Stream<T, E>, E>) -> Stream<T, E>
fn Future::fuse          (Future<T, E>)            -> Future<T, E>
fn Future::catch_unwind  (Future<T, E>+UnwindSafe) -> Future<Result<T, E>, Any+Send>
fn Future::shared        (Future<T, E>)            -> Future<SharedItem<T>, SharedError<E>>+Clone
fn Future::wait          (Future<T, E>)            -> Result<T, E>
"""[1:]

# RED = "#c82829" # code: types
# SCARLET = "#df3600" # doc: structs
# TANGO = "#e57300" # doc: type aliases
# ORANGE = "#ff9011" # code: question mark
# COPPER = "#b76514" # code: lifetimes
# BROWN = "#8c6067" # function names
# GREEN = "#718c00" # doc: literals
# FOREST = "#5e9766" # doc: enums
# CYAN = "#39a7bf" # doc: built-in types
# TEAL = "#3e999f" # code: macros
# BLUE = "#4271ae" # code: operators?
# PURPLE = "#7c5af3" # doc: traits
# AMETHYST = "#8959a8" # code: keywords
# GREY = "#8e908c" # code: comments

VERSION = "0.1.13"

import html, re, sys

def entry(m):
    name, = m.groups()
    m = re.match("Future::(.*)", name)
    if m:
        method, = m.groups()
        url = f"https://docs.rs/futures/{VERSION}/futures/future/trait.Future.html#method.{method}"
    else:
        url = f"https://docs.rs/futures/{VERSION}/futures/future/fn.{name}.html"
    return fr'<span style="color: #8959a8">fn</span> <a href="{url}">{name}</a>'

s = html.escape(s)

s = re.sub(r'(//.*)', r'<span style="color: #8e908c">\1</span>', s)
s = re.sub(r'\b([A-Z])\b', r'<var>\1</var>', s)
s = re.sub(r'\b(?:fn) ((?:\w+::)?\w+)\b', entry, s)
s = re.sub(r'\b(usize|SharedError|SharedItem|Task|Vec|Either|Loop|Result|Poll|'
           r'Any|Clone|Into|IntoIterator|Send|Stream|UnwindSafe)\b', r'<span style="color: #4271ae">\1</span>', s)
s = re.sub(r'\b(Future|IntoFuture)\b(?!\.html|::)', r'<span style="color: #c82829">\1</span>', s)
s = re.sub(r"(&#x27;static)\b", r'<span style="color: #b76514">\1</span>', s)
s = re.sub(r'\b(thread_local!)', r'<span style="color: #3e999f">\1</span>', s)
s = re.sub(r'\b(Fn|FnMut|FnOnce)\b', r'<span style="color: #8959a8">\1</span>', s)

with open(sys.argv[1], "w") as f:
    f.write("""<pre><code>{}</code></pre>""".format(s))
with open(re.match("(.*)\.include\.html$", sys.argv[1]).group(1) + ".html", "w") as f:
    f.write("""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title>Cheatsheet for Futures</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Fira+Mono|Fira+Sans|Oxygen"/>
    <link rel="stylesheet" href="/css/normalize.css"/>
    <link rel="stylesheet" href="/css/main.css"/>
  </head>
  <body><pre style="margin: 0"><code style="background: transparent">{}</code></pre></body>
</html>""".format(s))
