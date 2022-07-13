export type Ok<T> = {
    isOk: true
    data: T
}

export type Err<E> = {
    isOk: false
    reason: E
}

export type Result<T, E> =
    | Ok<T>
    | Err<E>

const ok = <T, E>(data: T): Result<T, E> => ({
    isOk: true,
    data,
});

const err = <T, E>(reason: E): Result<T, E> => ({
    isOk: false,
    reason,
});

const orElse = <T, E>(other: T) => (res: Result<T, E>): T =>
    res.isOk ? res.data : other;

export const result = {
    ok,
    err,
    orElse,
};
