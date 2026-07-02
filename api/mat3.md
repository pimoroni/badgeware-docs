---
title: mat3
summary: Defines 2D transformation matrices allowing shapes to be translated, rotated, scaled, or skewed during rendering.
icon: grid_3x3
publish: true
---
# Introduction
Matrices provide a unified way to handle transformations such as translation, rotation, scaling, and shearing. By combining these into a single matrix, you can apply complex transformations to vectors with a single operation.

Multiple transformations can also be chained together through matrix multiplication, making matrices both efficient and elegant tools for managing motion and geometry in 2D space.

# Methods
The following methods operate on matrices and return new matrices with the requested transformation applied. These methods can be chained to build up complex transformations.

## mat3()
Creates a new identity matrix.

### Usage
```python-raw
mat3()
```

### Returns
A `mat3` identity matrix.

## translate()
Returns a new matrix with a translation applied to the current matrix.

### Usage
```python-raw
.translate(x, y)
```

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` \| `float` | Amount to translate by |

### Returns
A `mat3` representing the translated matrix.

## rotate() / rotate_radians()
Returns a new matrix with a rotation applied to the current matrix. The angle is specified in degrees for `rotate()`; to work in radians, use `rotate_radians()`.

### Usage
```python-raw
.rotate(angle)
.rotate_radians(angle)
```

| Parameter | Type | Description |
|---|---|---|
| `angle` | `int` \| `float` | Rotation angle, in degrees for `rotate()` or radians for `rotate_radians()` |

### Returns
A `mat3` representing the rotated matrix.

## scale()
Returns a new matrix with a scale applied to the current matrix.

### Usage
```python-raw
.scale(x, y)
```

| Parameter | Type | Description |
|---|---|---|
| `x`, `y` | `int` \| `float` | Scale factors for the x and y axes |

### Returns
A `mat3` representing the scaled matrix.

## multiply()
Returns a new matrix with another matrix multiplied with the current matrix.

### Usage
```python-raw
.multiply(m)
```

| Parameter | Type | Description |
|---|---|---|
| `m` | `mat3` | The matrix to multiply with |

### Returns
A `mat3` representing the multiplied matrices.

## inverse()
Returns a new matrix that is the inverse of the current matrix. If the matrix is not invertible, the result is undefined.

### Usage
```python-raw
.inverse()
```

### Returns
A `mat3` that is the inverse of the current matrix.
