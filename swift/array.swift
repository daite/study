// Refer to https://developer.apple.com/documentation/swift/array

// initialize;
var arr1 = [1, 2, 3]
var arr2: [Int] = [1, 2, 3]
var arr3 = [Int]()

// multiple types
var arr4: [Any] = [1, "hello"]

// repeating
var arr5 = [Int](repeating: 3, count: 7) // [3, 3, 3, 3, 3, 3, 3]

// multi array
var marr: [[Int]] = [[1, 2, 3], [4, 5, 6]]

// access
print(arr1[0]) // 1
print(marr[1]) // [4, 5, 6]

// count
print(arr1.count) // 3

// empty?
print(arr1.isEmpty) // false

// shuffle
print(arr1.shuffled()) // [3, 1, 2]; random

// append
arr1.append(4) 
print(arr1) // [1, 2, 3, 4]

// merge
print(arr1 + [5, 6, 7, 8]) // [1, 2, 3, 4, 5, 6, 7, 8]

// insert
arr2.insert(-1, at: 1)
print(arr2) // [1, -1, 2, 3]

// replace
arr2[0] = -1
print(arr2) // [-1, -1, 2, 3]

// remove
print(arr1) // [1, 2, 3, 4]
arr1.remove(at: 2)
print(arr1) // [1, 2, 4]

// subarray
print(arr1[0...1]) // [1, 2]
print(arr1[0..<1]) // [1]

// bulk change
var a = [1, 2, 3, 4, 5]
a[1...3] = [12, 13]
print(a) // [1, 12, 13, 5]