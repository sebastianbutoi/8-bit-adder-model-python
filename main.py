# This function takes an input from the user and checks its value
# The input value cannot be greater than 255 since we are using a 8 bit format
def decimal_input():
    while True:
        try:
            x = int(input('Please enter a decimal number: '))
            if x > 255:
                print("The max number is 255. Please try again")
            else:
                break
        except ValueError:
            print("*** Warning! The input must be a integer number. Please insert the value again. ***")
    return x


# This function is used for the binary input and it performs some checks on the input
def binary_input():
    while True:
        x = str(input('Please enter a binary number using 8 bits or less: '))
        x = list(x)
        boolean = is_binary(x)

        if boolean and len(x) <= 8:
            string = ""
            for i in x[::-1]:
                string = string + str(i)
            string = list(string)
            while len(string) < 8:
                string.append('0')
            return list(reversed(string))
        elif boolean:
            print("\n*** Wrong input! You have inserted", len(x), "bits. The maximum length is 8 bits. Please try again. ***\n")
        else:
            print("\n*** Wrong input! The binary number contains only 0's and 1's. Please try again. ***\n")


# AND Gate
def and_gate(x, y):
    if x == '1' and y == '1':
        return '1'
    else:
        return '0'


# OR Gate
def or_gate(x, y):
    if x == '0' and y == '0':
        return '0'
    else:
        return '1'


# XOR Gate
def xor_gate(x, y):
    return or_gate(and_gate(x, not_gate(y)), and_gate(y, not_gate(x)))


# NOT Gate
def not_gate(x):
    if x == '1':
        return '0'
    else:
        return '1'


# This function will calculate the carry value
def calculate_carry(x, y, z, w):
    return or_gate(and_gate(x, y), and_gate(z, w))


# This function will calculate the sum using the logical gates
def calculate_sum(x, y):
    result = []
    carry = 0
    for i in range(len(x)):
        result.append(xor_gate(xor_gate(x[i], y[i]), carry))
        carry = calculate_carry(x[i], y[i], xor_gate(x[i], y[i]), carry)

    # If the final carry is 1 then it will be added to the list and the result 
    # will have 9 bits, otherwise the result will be represented using 8 bits
    if carry == '1':
        result.append(carry)

    return list(reversed(result))


# This function will convert the decimal number into binary using a 8 bit representation
def decimal_to_binary(x):
    v = []
    while x > 0:
        a = int(x % 2)
        v.append(a)
        x = (x - a) / 2

    # Make sure the list has 8 bits
    while len(v) < 8:
        v.append('0')

    # Reverse the list
    string = ""
    for i in v[::-1]:
        string = string + str(i)
    string = list(string)

    return string


# This function will convert a binary number into a decimal number
def binary_to_decimal(x):
    n = 0
    for i in range(len(x)):
        n = n*2 + int(x[i])

    return n


# This function calculates the first complement
# e.g. 1st complement of 0010010 will be 1101101
def first_complement(x):
    for i in range(len(x)):
        if x[i] == '0':
            x.insert(i, '1')
            x.pop(i+1)
        else:
            x.insert(i, '0')
            x.pop(i+1)

    return x


# This function calculates the second complement
# 2nd complement = 1st complement + 1
def second_complement(x):
    v = ['0', '0', '0', '0', '0', '0', '0', '1']
    return calculate_sum(list(reversed(x)), list(reversed(v)))


# This function calculates the subtraction between two numbers
def calculate_subtraction(x, y):
    sub = calculate_sum(list(reversed(x)), list(reversed(y)))
    sub.pop(0)
    return list(reversed(sub))


# This function checks if the list contains 0's and 1's
# It returns False if it finds a different character from 0 and 1
# If there are only 0's or 1's, then the function returns True
def is_binary(x):
    return set(x) <= set('01')


# This function finds which decimal number is negative and calculates
# the 2nd complement of the negative number.
# If both input numbers will be negative then the function will calculate
# the 2nd complement of both of them
def find_the_negative(x, y):
    # If x is negative then calculate its 2nd complement
    if x < 0 and y > -1:
        second_comp = second_complement(first_complement(decimal_to_binary(x * (-1))))
        y = decimal_to_binary(y)
        return second_comp, y

    # If y is negative then calculate its 2nd complement
    if y < 0 and x > -1:
        second_comp = second_complement(first_complement(decimal_to_binary(y * (-1))))
        x = decimal_to_binary(x)
        return x, second_comp

    # If both x and y are negative then calculate the 2nd complement of both
    if x < 0 and y < 0:
        second_comp_x = second_complement(first_complement(decimal_to_binary(x * (-1))))
        second_comp_y = second_complement(first_complement(decimal_to_binary(y * (-1))))
        return second_comp_x, second_comp_y


def main():
    while True:
        while True:
            try:
                choice = int(input("Insert 1 for decimal input or 2 for binary input: "))
                # Input 1 - decimal format input
                if choice == 1:
                    # Input of two decimal number
                    print("\n")
                    first_number = decimal_input()
                    second_number = decimal_input()
                    # If there is any negative number use the 2nd complement to convert them into binary
                    if first_number < 0 or second_number < 0:
                        x, y = find_the_negative(first_number, second_number)
                    else:
                        # If the input numbers are positive then convert them into binary
                        x = decimal_to_binary(first_number)
                        y = decimal_to_binary(second_number)
                    break
                # Input 2 - binary format input
                if choice == 2:
                    print("\n")
                    x = binary_input()
                    y = binary_input()
                    break
                # If the input will be different from 1 or 2 then a suitable message will be displayed
                print("\n*** Wrong input! Please try again. ***\n")
            except ValueError:
                # If the user inserts a string or a different number format (e.g. double) then a suitable message will be displayed
                print("\n*** You must insert a number. In this case it must be 1 or 2.** \n")

        # Data process and output for the decimal input
        if choice == 1:
            # Calculate the sum between the two binary values
            sum_result = calculate_sum(list(reversed(x)), list(reversed(y)))

            # Subtraction using the 1st complement and 2nd complement
            subtraction_result = list(reversed(calculate_subtraction(x, second_complement(first_complement(y)))))

            # Print the values
            print("\nThe sum of", first_number, "and", second_number, "is:", first_number + second_number)
            print("The binary representation of", first_number + second_number, "is:", ''.join(str(i) for i in sum_result))
            print("The subtraction of", first_number, "and", second_number, "is:", first_number - second_number)
            print("The binary representation of", first_number - second_number, "is:", ''.join(str(i) for i in subtraction_result))

        # Data process and output for the binary input
        if choice == 2:
            # Calculate the sum between the two binary values
            sum_result = calculate_sum(list(reversed(x)), list(reversed(y)))

            # Subtraction using the 1st complement and 2nd complement
            subtraction_result = list(reversed(calculate_subtraction(x, second_complement(first_complement(y)))))

            # Print the values
            print("\nYou have inserted the values", binary_to_decimal(x), "and", binary_to_decimal(first_complement(y)), "in binary")
            print("The sum of the two numbers is", binary_to_decimal(sum_result))
            print("The sum in binary is", ''.join(str(i) for i in sum_result))
            print("The subtraction of", binary_to_decimal(x), "and", binary_to_decimal(y), "is", binary_to_decimal(x)-binary_to_decimal(y))
            print("The subtraction in binary is", ''.join(str(i) for i in subtraction_result))

        # Exit or restart the program
        quit_program = input("\nPress q if you want to quit the program or press any other key to restart it:")

        if quit_program == 'q':
            print("\nThank you for using this program. Have a good day!")
            break
        else:
            print("")


if __name__ == "__main__":
    main()


