from collections import OrderedDict
import os

def split_lines(path):
    year = open(path, 'r')
    data = year.readlines() #data in the format of strings in list

    Dict = OrderedDict()
    for line in data :
        dash_index = line.index('-')
        ending = len(line) - 1

        first_half = line[0:dash_index]
        second_half = line[dash_index + 1:ending].strip()

        Dict[first_half] = second_half.lower()

    #returns in Date:Comment format
    return Dict

#Defines the dictionary
def define_dic() :

    #Array of emotions
    emotions = ['great','good','ok','meh','anxious','n/a','sad','rough','depressed','aight','angry'
                ,'overwhelmed','off','shitty','stressed','content','average','shit','decent','awesome',
                'above average','neutral','hard','tired','nice','fun','unreal','alright','chill']

    count_dic = {emotion: 0 for emotion in emotions}
    return count_dic

def count_dict_vals(count_dic) :
    count = 0
    for key in count_dic:
        if(count_dic[key] > 0):
            count += count_dic[key]

    return count

#Starts with data dictionary, returns with count of each emotion
def clean_values(global_perps, file_name,data_dict):

    # Create temp dic
    data_count_dic = define_dic()

    for key in data_dict:
        # Create temp dic
        count_dic = define_dic()
        #comment next to date
        value = data_dict[key]


        if(len(value) > 1):

            count_dic = {emotion: value.count(emotion) for emotion in count_dic}

            if(sum(count_dic.values()) != 1) :
                #For now, just list offending perps, keep this for wwhen count is 0
                data_dict[key] = '{} <----- EMOTION COUNT = {}'.format(value, sum(count_dic.values()))
                update_perps(global_perps,file_name,key,data_dict[key])
            else :
                # merge temp dic with function data count dic
                merge_dicts(data_count_dic, count_dic)



        #No comment, assume N/A
        else:
            count_dic['n/a'] += 1
            # merge temp dic with function data count dic
            merge_dicts(data_count_dic, count_dic)
            #update_perps(global_perps, file_name, key, data_dict[key])


    return data_count_dic


#Merges each year dictionary count into one global dictionary
def merge_dicts(global_count_dic,count_dic):
    for key in global_count_dic :
        global_count_dic[key] += count_dic[key]

#Prints the data
def print_data(year_dict):
    count = 0
    for key in year_dict:
        print("{}  {} ---> {}".format(count, key, year_dict[key]))
        count += 1




def main():

    ###########Variables##############
    data_2019 = split_lines('data/data2019.txt')
    data_2020 = split_lines('data/data2020.txt')
    data_2021 = split_lines('data/datahalf2021.txt')

    #list of dictionaries of data
    data_dic_list = []

    #list of dictionary of count of each emotion
    count_dic_list = []
    # Will Have Final values
    global_dic = define_dic()

    #Where there are discrepancies in data
    # Structure to determining unparsable data:
    # 1. File it occured in
        # 2. Date + Comment
    global_perps = []

    #path to data files
    data_path = '{}/{}'.format(os.getcwd(), 'data')
    data_list = os.listdir(data_path)

    #List of file names we will be analyzing
    user_list = []
    ##################################

    print('######################################################')
    print('Hello, and welcome to year analyzed.')
    print('This cute lil python app turns daily emotion data into something meaningful.')
    print('Put data in the data folder.')
    print('######################################################')

    opt1 = raw_input('How many years would you like to do? Enter # or A for all:')

    if(opt1.isdigit()) :
        #convert to integer
        opt1 = int(opt1)

        print('Available Options:')

        for i in range(len(data_list)):
            print('{} : {}'.format(i + 1,data_list[i]))
        print(' ')

        for i in range(opt1):
            #Get names of data files and store in list
            file_index = input('Enter file #{}: '.format(i+1))
            a_file = data_list[file_index - 1]

            #Append to list of files we will manipulate
            user_list.append(a_file)
            #Append to list of potential files where perps may be found
            temp_list = [a_file]
            global_perps.append(temp_list)


    else :
            #Get all file names
            print('Decided to choose all files in data dir...')
            user_list = data_list

            #Instantiate list in each onee of the files
            for i in range(len(global_perps)):
                temp_list = [data_list[i]]
                global_perps.append(temp_list)

    #Input data from files
    for i in range(len(user_list)):
        data_dic_list.append(split_lines('{}/{}'.format('data',user_list[i])))

    #1. Convert data into dictionary of emotions, store in list
    for i in range(len(data_dic_list)):
        count_dic_list.append(clean_values(global_perps,user_list[i],data_dic_list[i]))
        # 2. Merge this count dictionary with the global one
        merge_dicts(global_dic, count_dic_list[i])

    #3. Print this data meaningfully.
    
    f = open("guru99.txt", "w+")
    #for i in range(len(data_dic_list)):
        #print_data(data_dic_list[i])

    #for key in global_dic :
        #print('{}: {}'.format(key,global_dic[key]))



    print('{} days accounted for error free.'.format(count_dict_vals(global_dic)))
    print('{} days not accounted for.'.format(len(global_perps[0])-1))

    for i in range(len(global_perps)):
        #print first index in list of list
        print('In File {}:'.format(global_perps[i][0]))
        count = 0
        for j in range(len(global_perps[i]) - 1):
            #print from 1,x
            print('    {}'.format(global_perps[i][j + 1]))
            count += 1

#Update list of unparsable instances
def update_perps(global_perps, file_name, key, value):

    find_index = -1

    #find list where first index is the file name
    for i in range(len(global_perps)) :
        if global_perps[i][0] is file_name :
            find_index = i

    if find_index != -1 :
        global_perps[find_index].append('{}{}'.format(key,value))
    else:
        print('Could not find file name in global perp list')





main()


