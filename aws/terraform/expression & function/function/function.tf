variable "first_list" {
  default = ["apple", "banana"]
}

variable "second_list" {
  default = ["cherry", "date"]
}

variable "input_string" {
  default = "apple,banana,cherry,date"
}

# Concat 함수: 두 개의 리스트를 연결하여 하나의 리스트로 만듦
output "combined_list" {
  value = concat(var.first_list, var.second_list)
}

# Startswith 함수: 문자열이 특정 접두사로 시작하는지 확인
output "startswith_check" {
  value = startswith("apple pie", "apple")
}

# Toset 함수: 리스트를 집합으로 변환하여 중복 제거
variable "list_with_duplicates" {
  default = ["apple", "banana", "apple", "cherry"]
}

output "unique_set" {
  value = toset(var.list_with_duplicates)
}

# Length 함수: 리스트나 문자열의 길이를 반환
output "list_length" {
  value = length(var.first_list)
}

# Split 함수: 문자열을 구분자로 나눠 리스트로 변환
output "split_list" {
  value = split(",", var.input_string)
}
