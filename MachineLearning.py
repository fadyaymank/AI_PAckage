import math


class item:
    def __init__(self, age, prescription, astigmatic, tearRate, needLense):
        self.age = age
        self.prescription = prescription
        self.astigmatic = astigmatic
        self.tearRate = tearRate
        self.needLense = needLense

def getDataset():
    data = []
    labels = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0]
    data.append(item(0, 0, 0, 0,	labels[0]))
    data.append(item(0, 0, 0, 1,	labels[1]))
    data.append(item(0, 0, 1, 0,	labels[2]))
    data.append(item(0, 0, 1, 1,	labels[3]))
    data.append(item(0, 1, 0, 0,	labels[4]))
    data.append(item(0, 1, 0, 1,	labels[5]))
    data.append(item(0, 1, 1, 0,	labels[6]))
    data.append(item(0, 1, 1, 1,	labels[7]))
    data.append(item(1, 0, 0, 0,	labels[8]))
    data.append(item(1, 0, 0, 1,	labels[9]))
    data.append(item(1, 0, 1, 0,	labels[10]))
    data.append(item(1, 0, 1, 1,	labels[11]))
    data.append(item(1, 1, 0, 0,	labels[12]))
    data.append(item(1, 1, 0, 1,	labels[13]))
    data.append(item(1, 1, 1, 0,	labels[14]))
    data.append(item(1, 1, 1, 1,	labels[15]))
    data.append(item(1, 0, 0, 0,	labels[16]))
    data.append(item(1, 0, 0, 1,	labels[17]))
    data.append(item(1, 0, 1, 0,	labels[18]))
    data.append(item(1, 0, 1, 1,	labels[19]))
    data.append(item(1, 1, 0, 0,	labels[20]))
    return data


class Feature:
    def __init__(self, name):
        self.name = name
        self.visited = -1
        self.infoGain = -1


class Node:
    def __init__(self, name='', column_index=-1, pure=0, decision=-1):
        self.name = name
        self.column_index = column_index
        self.pure = pure
        self.decision = decision
        self.right = []
        self.left = []


class ID3:
    def __init__(self, features):
        self.features = features
        self.tree_root = []
        self.build_decision_tree(self.construct_2D_array(dataset), self.tree_root)

    def construct_2D_array(self, dataset):
        data_2D = []
        for i in range(0, len(dataset)):
            lst = [dataset[i].age, dataset[i].prescription, dataset[i].astigmatic, dataset[i].tearRate, dataset[i].needLense]
            data_2D.insert(i, lst)
        return data_2D

    def entropy(self, column_index, current_items):
        #  total entropy
        total = len(current_items)
        need = 0
        no_need = 0
        zero_need = 0
        one_need = 0
        zero_no_need = 0
        one_no_need = 0
        decision_col = len(current_items[0]) - 1
        for i in range(0, len(current_items)):
            if current_items[i][decision_col] == 0:
                no_need += 1
                if current_items[i][column_index] == 1:
                    one_no_need += 1
                else:
                    zero_no_need += 1
            else:
                need += 1
                if current_items[i][column_index] == 1:
                    one_need += 1
                else:
                    zero_need += 1
        total_entropy = 0
        if need != total and need != 0:
            total_entropy += (-need / total) * math.log((need / total), 2)
        if no_need != total and no_need != 0:
            total_entropy += (-no_need / total) * math.log((no_need / total), 2)

        zero_entropy = 0
        total_zero = zero_need + zero_no_need
        if total_zero > 0:
            p_zero_need = zero_need / total_zero
            p_zero_no_need = zero_no_need / total_zero
            if p_zero_need != 1 and p_zero_need != 0:
                zero_entropy += -p_zero_need * math.log(p_zero_need, 2)
            if p_zero_no_need != 1 and p_zero_no_need != 0:
                zero_entropy += -p_zero_no_need * math.log(p_zero_no_need, 2)

        one_entropy = 0
        total_one = one_need + one_no_need
        if total_one > 0:
            p_one_need = one_need / total_one
            p_one_no_need = one_no_need / total_one
            if p_one_need != 1 and p_one_need != 0:
                one_entropy += -p_one_need * math.log(p_one_need, 2)
            if p_one_no_need != 1 and p_one_no_need != 0:
                one_entropy += -p_one_no_need * math.log(p_one_no_need, 2)

        return total_entropy, total_zero, zero_entropy, total_one, one_entropy

    def info_gain(self, column_index, current_items):
        total_entropy, total_zero, zero_entropy, total_one, one_entropy = self.entropy(column_index, current_items)
        total = len(current_items)
        gain = total_entropy - (total_zero / total * zero_entropy + total_one / total * one_entropy)
        return gain

    def split(self, data, column_index):
        data0 = []
        data1 = []
        for i in range(0, len(data)):
            row = data[i]
            if data[i][column_index] == 0:
                data0.insert(i, row)
            else:
                data1.insert(i, row)
        return data0, data1

    def build_decision_tree(self, data, current_node):
        # checking for purity
        decision_col = len(data[0]) - 1
        zeroes = 0
        for i in range(0, len(data)):
            if data[i][decision_col] == 0:
                zeroes += 1

        if zeroes == 0:
            current_node.append(Node('', -1, 1, 1))
            return
        if zeroes == len(data):
            current_node.append(Node('', -1, 1, 0))
            return

        max_gain = -1
        max_feature = -1
        for feature_index in range(0, len(self.features)):
            if self.features[feature_index].visited == 1:
                continue
            gain = self.info_gain(feature_index, data)
            self.features[feature_index].info_gain = gain
            if gain > max_gain:
                max_gain = gain
                max_feature = feature_index
        current_node.append(Node(self.features[max_feature].name, max_feature, 0, -1))
        features[max_feature].visited = 1
        data0, data1 = self.split(data, max_feature)
        self.build_decision_tree(data0, current_node[0].left)
        self.build_decision_tree(data1, current_node[0].right)

    def classify(self, input):
        # takes an array for the features ex. [0, 0, 1, 1]
        # should return 0 or 1 based on the classification
        current_node = self.tree_root
        while not current_node[0].pure:
            if input[current_node[0].column_index]:
                current_node = current_node[0].right
            else:
                current_node = current_node[0].left
        return current_node[0].decision


dataset = getDataset()
features = [Feature('age'), Feature('prescription'), Feature('astigmatic'), Feature('tearRate')]
id3 = ID3(features)
cls = id3.classify([0, 0, 1, 1]) # should print 1
print('testcase 1: ', cls)
cls = id3.classify([1, 1, 0, 0]) # should print 0
print('testcase 2: ', cls)
cls = id3.classify([1, 1, 1, 0]) # should print 0
print('testcase 3: ', cls)
cls = id3.classify([1, 1, 0, 1]) # should print 1
print('testcase 4: ', cls)
