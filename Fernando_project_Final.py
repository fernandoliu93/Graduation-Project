# @Author  : Fengzhang Liu
# @Project : An Interactive System For Terms And Substitutions


theta_dict = {}
abc_dict = {}
judgeType = 0
result = ''
resultJudge = 0
new_result = ''

unify_result = ''
unify_stack = []
unify_type = "common"
unify_dict = {}

#Defining Node
class Node:
    def __init__(self, v):
        self.v = v
        self.left = None
        self.right = None

#Determine if it is a constant
def isusual(key):
    return len(key) == 1 and key.islower()

#Print tree for size and height
def print_tree(root):
    if root.left != None and root.right != None:
        return root.v + '(' + print_tree(root.left) + ',' + print_tree(root.right) + ')'
    if root.left != None and root.right == None:
        return root.v + '(' + print_tree(root.left) + ')'
    if root.left == None and root.right != None:
        return root.v + '(' + print_tree(root.right) + ')'
    if root.left == None and root.right == None:
        return root.v

#build tree for size and height
def build(expression):
    if expression is None or len(expression) == 0:
        return None

    i1 = expression.find('(')

    if i1 < 0:
        root = Node(expression)
        return root
    else:
        f_name = expression[:i1]
        exp = expression[i1 + 1:-1]

        root = Node(f_name)

        si = -1
        stack = []
        for i in range(len(exp)):
            if len(stack) == 0 and exp[i] == ',':
                si = i
                break
            elif exp[i] == '(':
                stack.append(exp[i])
            elif exp[i] == ')':
                stack.pop()
        if si != -1:
            root.left = build(exp[:si].strip())
            root.right = build(exp[si + 1:].strip())
        else:
            root.left = build(exp)
        return root

#get size
def getSize(root):
    if root: return 1 + getSize(root.left) + getSize(root.right)
    return 0

#get height
def getHeight(root):
    if root:
        return max((1 + getHeight(root.left)), (1 + getHeight(root.right)))
    return -1

#Judging the structure of the tree
def judge(s, t):
    global result
    global judgeType
    if (s.left or s.right) and (t.left or t.right):
        if s.v != t.v:
            judgeType = 1
        else:
            judge(s.left, t.left)
            judge(s.right, t.right)
    else:
        _t = str(t.v)
        _s = str(s.v)
        if t.left:
            _t = str(t.v) + '(' + str(t.left.v) + ')'
        if s.left:
            _s = str(s.v) + '(' + str(s.left.v) + ')'

        result = result + "," + _t + "=" + _s


def pre(s):
    if 'x' in s: return False
    if 'y' in s: return False
    if 'z' in s: return False
    return True

#Initialize variables
def init():
    global resultJudge
    global new_result
    global judgeType
    global result
    global unify_result
    global unify_stack
    global unify_type
    global unify_dict

    resultJudge = 0
    new_result = ''
    judgeType = 0
    result = ''
    unify_result = ''
    unify_stack = []
    unify_dict = {}
    unify_type = "common"


def judgeResult(string):
    global resultJudge
    x = ''
    y = ''
    z = ''
    global new_result
    list = string.split(',')
    if len(list) == 2:
        if list[0][0] == list[1][0] and list[0].split('=')[1] in list[1].split('=')[1] or list[1].split('=')[1] in \
                list[0].split(
                    '=')[1]: resultJudge = 1
        if list[0][-1] == list[1][-1] and list[0].split('=')[0] in list[1].split('=')[0] or list[1].split('=')[0] in \
                list[0].split(
                    '=')[0]: resultJudge = 1
    for i in range(len(list)):
        if list[i][0] == 'x' and pre(list[i].split('=')[1]):
            x = list[i].split('=')[1]
        if list[i][0] == 'y' and pre(list[i].split('=')[1]):
            y = list[i].split('=')[1]
        if list[i][0] == 'z' and pre(list[i].split('=')[1]):
            z = list[i].split('=')[1]
        if list[i][-1] == 'x' and pre(list[i].split('=')[0]):
            x = list[i].split('=')[0]
            list[i] = list[i].split('=')[1] + '=' + list[i].split('=')[0]
        if list[i][-1] == 'y' and pre(list[i].split('=')[0]):
            y = list[i].split('=')[0]
            list[i] = list[i].split('=')[1] + '=' + list[i].split('=')[0]
        if list[i][-1] == 'z' and pre(list[i].split('=')[0]):
            z = list[i].split('=')[0]
            list[i] = list[i].split('=')[1] + '=' + list[i].split('=')[0]

    if x == '':
        for i in range(len(list)):
            if list[i][-1] == 'x':
                list[i] = list[i].split('=')[1] + '=' + list[i].split('=')[0]
    if y == '':
        for i in range(len(list)):
            if list[i][-1] == 'y':
                list[i] = list[i].split('=')[1] + '=' + list[i].split('=')[0]
    if z == '':
        for i in range(len(list)):
            if list[i][-1] == 'z':
                list[i] = list[i].split('=')[1] + '=' + list[i].split('=')[0]
    for i in range(len(list)):
        if not pre(list[i].split('=')[0]):
            list[i] = list[i].split('=')[0] + '=' + list[i].split('=')[1].replace('x', x)
            list[i] = list[i].split('=')[0] + '=' + list[i].split('=')[1].replace('y', y)
            list[i] = list[i].split('=')[0] + '=' + list[i].split('=')[1].replace('z', z)
            # print(list[i])
            new_result = new_result + ',' + list[i]

    return 0

#Determine input is correct or not
def judge_r(line):
    kuohao = 0
    kuohao2 = 0
    for i in range(len(line)):
        if line[i] == '(': kuohao += 1
        if line[i] == ')': kuohao -= 1
        if line[i] == '{': kuohao2 += 1
        if line[i] == '}': kuohao2 -= 1
    if kuohao == 0 and kuohao2 == 0:
        if 'apply' in line:
            if 'theta' in line.split(',')[0] and 'theta' not in line.split(',')[1]: return True
            if 'sigma' in line.split(',')[0] and 'sigma' not in line.split(',')[1]: return True
        if 'compose' in line:
            if 'theta' in line.split(',')[0] and 'theta' in line.split(',')[1]: return True
            if 'sigma' in line.split(',')[0] and 'sigma' in line.split(',')[1]: return True
        if 'size' in line:
            if 'theta' not in line and 'sigma' not in line: return True
            # if 'sigma' not in line: return True
        if 'height' in line:
            if 'theta' not in line and 'sigma' not in line: return True
            # if 'sigma' not in line: return True
        if 'unify' in line:
            if 'theta' not in line.split(',')[0] and 'theta' not in line.split(',')[1] and 'sigma' not in \
                    line.split(',')[0] and 'sigma' not in line.split(',')[1]: return True
        if '=' in line: return True
    return False

#Judge the operation
def operation(line):
    if 'apply' in line: return True
    if 'compose' in line: return True
    if 'size' in line: return True
    if 'height' in line: return True
    if 'unify' in line: return True
    return False

#Judge the balance of the tree
def split_theta(line):
    # x:=h(a,c),y:=b,z:=c
    result = []
    balance = 0
    record = 0
    for i in range(len(line)):
        if line[i] == '(': balance += 1
        if line[i] == ')': balance -= 1
        if line[i] == ',' and balance == 0:
            temp = line[record:i]
            record = i + 1
            result.append(temp)
        if i == len(line) - 1: result.append(line[record:])
    return result

#unify function
def unify(s, t):
    global unify_type
    global unify_stack

    if s is not None and t is not None:
        # print(print_tree(s))
        # print(print_tree(t))
        if s.v == t.v and s.left is None and s.right is None and t.left is None and t.right is None: return
        if s.v != t.v:
            if s.v in print_tree(t) and isusual(s.v):
                unify_type = "Function Clash"
                return
            if s.v in print_tree(t) and (not isusual(s.v)):
                unify_type = "Occur-Check"
                return
            if t.v in print_tree(s) and isusual(t.v):
                unify_type = "Function Clash"
                return
            if t.v in print_tree(s) and (not isusual(t.v)):
                unify_type = "Occur-Check"
                return

            judge1 = print_tree(s) + ':=' + print_tree(t)
            judge2 = print_tree(t) + ':=' + print_tree(s)
            t1 = print_tree(s)
            t2 = print_tree(t)
            if (isusual(t1) and not t2.isupper()) or ((isusual(t2) and not t1.isupper())):
                unify_type = "Not Unifiable"
                return
            if '(' in t1 and '(' in t2:
                unify_type = "Function Clash"
                return
            temp = t1 + ':=' + t2
            if '(' in t1: temp = t2 + ':=' + t1  # t1 is g(x)
            if isusual(t1) and t2.isupper(): temp = t2 + ':=' + t1  # t1 is usual
            # print("temp"+temp)
            if judge1 not in unify_stack and judge2 not in unify_stack and t1 != t2:
                unify_stack.append(temp)
            return
        else:
            unify(s.left, t.left)
            unify(s.right, t.right)
    else:
        return

#Merge after unify
def combine():
    global unify_type
    global unify_stack

    if not unify_stack: return
    end = False
    temp = unify_stack
    while not end:
        for i in unify_stack:
            left = i.split(':=')[0]
            right = i.split(':=')[1]
            if isusual(left) and isusual(right):
                unify_type = "Not Unifiable"
                return
            if left.isupper():
                for j in unify_stack:
                    # % s = f(X, g(X))
                    # % t = f(Y, Y)
                    # % unify(s, t)
                    if j != i:
                        left_j = j.split(':=')[0]
                        right_j = j.split(':=')[1]
                        if left_j == left:
                            unify_stack.remove(j)
                            s = build(right)
                            t = build(right_j)
                            unify(s, t)
                        if right_j == left:
                            unify_stack.remove(j)
                            s = build(right)
                            t = build(left_j)
                            unify(s, t)
            if temp == unify_stack:
                end = True
            else:
                temp = unify_stack
    return

#Organize the merged result set
def clean():
    # % s = h(f(X), Y)
    # % t = h(Y, f(Z))
    # % unify(s, t)
    global unify_stack
    move = False
    for i in unify_stack:
        left = i.split(':=')[0]
        right = i.split(':=')[1]
        for j in unify_stack:
            if j != i:
                left_j = j.split(':=')[0]
                right_j = j.split(':=')[1]
                if left in right_j and right.isupper():
                    move = True
        if move:
            unify_stack.remove(i)
            unify_stack.append(right + ":=" + left)
            move = False
    new = ""
    for i in unify_stack:
        left = i.split(':=')[0]
        right = i.split(':=')[1]
        for j in unify_stack:
            if j != i:
                left_j = j.split(':=')[0]
                right_j = j.split(':=')[1]
                if left_j in right:
                    new = left + ":=" + right.replace(left_j, right_j)
        if new != "":
            unify_stack.remove(i)
            unify_stack.append(new)
            new = ""

    hasCircle=False
    sign=[]
    for i in unify_stack:
        left = i.split(':=')[0]
        right = i.split(':=')[1]
        if left.isupper() and right.isupper():
            for j in unify_stack:
                if j != i:
                    left_j = j.split(':=')[0]
                    right_j = j.split(':=')[1]
                    if left_j.isupper() and right_j.isupper():
                        if left==left_j:
                            hasCircle=True
                            sign.append(left)
                            sign.append(right)
                            sign.append(right_j)

    if hasCircle:
        for i in range(len(unify_stack)):
            left = unify_stack[i].split(':=')[0]
            right = unify_stack[i].split(':=')[1]
            if left in sign or right in sign:
                sign.append(left)
                sign.append(right)
    fsign = []
    for i in sign:
        if i not in fsign:fsign.append(i)
    # print(fsign)

    l = len(unify_stack)
    for i in range(l):
        left = unify_stack[l-1-i].split(':=')[0]
        right = unify_stack[l-1-i].split(':=')[1]
        if left.isupper() and right.isupper():
            if left in fsign and right in fsign:
                unify_stack.remove(unify_stack[l-1-i])
    for i in range(len(fsign)-1):
        unify_stack.append(fsign[i]+":="+fsign[len(fsign)-1])


# % s=f(X,f(Y,f(Z,U)))
# % t=f(Y,f(Z,f(U,X)))
# % unify(s,t)





#Logical control
while True:
    print("%", end=' ')
    line = input().replace(' ', '')
    if 'exit' in line: break
    if judge_r(line):
        if operation(line):
            if 'apply' in line:
                temp_theta = theta_dict.get(line.split('(')[1].split(',')[0])
                size = temp_theta.count(':')
                if size == 1:
                    temp_key = temp_theta.split(':')[0]
                    temp_value = temp_theta.split('=')[1]
                    temp_f = abc_dict.get(line.split(',')[1].replace(')', ''))
                    print(temp_f.replace(temp_key, temp_value))
                else:
                    result = split_theta(temp_theta)
                    temp_f = abc_dict.get(line.split(',')[1].replace(')', ''))
                    for i in range(len(result)):
                        temp_key = result[i].split(':')[0]
                        temp_value = result[i].split('=')[1]
                        temp_f = temp_f.replace(temp_key, temp_value)
                    print(temp_f)
            if 'compose' in line:
                temp_theta1 = theta_dict.get(line.split('(')[1].split(',')[0])
                temp_theta2 = theta_dict.get(line.split(',')[1].replace(')', ''))
                size = temp_theta1.count(':')
                if size == 1:
                    temp_key = temp_theta1.split(':')[0]
                    temp_value = temp_theta1.split('=')[1]
                    if temp_theta1 == temp_theta2:
                        if temp_key in temp_theta1.split('=')[1]:
                            print('{' + temp_theta1.split('=')[0] + '=' + temp_theta1.split('=')[1].replace(temp_key,
                                                                                                            temp_value) + '}')
                        else:
                            print('{' + temp_theta1 + '}')
                    else:
                        if temp_key in temp_theta2:
                            if temp_key in temp_theta2.split('=')[0] and temp_key in temp_theta2.split('=')[1]:
                                print(
                                    '{' + temp_theta2.split('=')[0] + '=' + temp_theta2.split('=')[1].replace(temp_key,
                                                                                                              temp_value) + '}')
                            else:
                                print(
                                    '{' + temp_theta2.split('=')[0] + '=' + temp_theta2.split('=')[1].replace(temp_key,
                                                                                                              temp_value) + ',' + temp_theta1 + '}')
                        else:
                            print('{' + temp_theta2 + ',' + temp_theta1 + '}')
                else:
                    result = split_theta(temp_theta1)
                    todo = split_theta(temp_theta2)
                    stack = []
                    has_add = [0 for i in range(len(todo))]
                    for i in range(len(todo)):
                        for j in range(len(result)):
                            temp_key = result[j].split(':')[0]
                            temp_value = result[j].split('=')[1]
                            todo_right = todo[i].split('=')[1]
                            if temp_key in todo_right:
                                if has_add[i] == 0:
                                    stack.append(todo[i].split('=')[0] + '=' + todo_right.replace(temp_key, temp_value))
                                    has_add[i] = 1
                                continue
                        if has_add[i] == 0:
                            stack.append(todo[i])
                    filter_set = []
                    for i in range(len(stack)):
                        if stack[i].split(':')[0] != stack[i].split('=')[1]:
                            filter_set.append(stack[i])
                    to_print = '{'
                    for x in filter_set:
                        to_print = to_print + x + ','
                    if to_print[-1] == ',':
                        to_print = to_print[:-1]
                    print(to_print + '}')
            if 'size' in line:
                temp_abc = abc_dict.get(line.split('(')[1].replace(')', ''))
                root = build(temp_abc)
                print('size:' + str(getSize(root)))
            if 'height' in line:
                temp_abc = abc_dict.get(line.split('(')[1].replace(')', ''))
                root = build(temp_abc)
                print('height:' + str(getHeight(root)))
            if 'unify' in line:
                temp_s = line.split('(')[1].split(',')[0]
                temp_t = line.split(',')[1].replace(')', '')
                # % s = f(x, f(g(x), b))
                # % t = f(a, f(Y, Y))
                # % unify(s, t)

                # % s = f(X, X)
                # % t = f(f(Y, Z), f(Z, h(Y)))
                # % unify(s, t)
                s = build(abc_dict.get(temp_s))
                t = build(abc_dict.get(temp_t))
                unify(s, t)
                combine()
                clean()
                if unify_type == "Function Clash":
                    print("Function Clash")
                elif unify_type == "Occur-Check":
                    print("Occur-Check")
                elif unify_type == "Not Unifiable":
                    print('Function Clash')
                else:
                    for x in unify_stack:
                        unify_result = unify_result + x + ','
                    print('{' + unify_result[:-1] + '}')
                init()
        else:
            if 'theta' in line or 'sigma' in line:
                theta_dict[line.split('=')[0]] = line.split('{')[1].replace('}', '')
            else:
                abc_dict[line.split('=')[0]] = line.split('=')[1]
    else:
        print('wrong input')
