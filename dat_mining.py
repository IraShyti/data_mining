import github
import operator
import datetime
import matplotlib.pyplot as plt
import networkx as NX

'''****
Data mining!!
MINING CHROMIUM REPOSITORY USING PYTHON
14.05.2016
IRA SHYTI
****'''
accounts = {"social": '',}

token = accounts["social"]
client = github.Github(token, per_page=100)
screen_name = "CreateJS"
repository_name = "AdobeAnimateDemo"

user = client.get_user(screen_name)
repo = user.get_repo(repository_name)

while (True):
    first_commit_date = raw_input("Please give the date of first commit (Format: YYYY-MM-DD): ")
    try:
        datetime.datetime.strptime(first_commit_date, '%Y-%m-%d')
        break
    except:
        print "Incorrect data format, should be YYYY-MM-DD"

user_list = dict()
commit_list = []
name_list = []
count = 0

#to get commiters, date of commit and commited files
print "Getting commit objects from repo. It may take a while... "
for commit in repo.get_commits():
    if commit.commit is not None:
        authorOfCommit = commit.commit.author
        if str(authorOfCommit.date) > first_commit_date:
            if authorOfCommit.name in user_list:
                user_list[authorOfCommit.name] += 1
            else:
                user_list[authorOfCommit.name] = 1
            commit_list.append([authorOfCommit.name])
            commit_list[count].append(str(authorOfCommit.date))
            name_list = commit.files
            for i in range(len(name_list)):
                commit_list[count].append(name_list[i].filename)
            count += 1
        else:
            break

file0 = open("Group3_Commits.txt", "w")
for i in commit_list:
    file0.write(str(i[0]) + "    " + str(i[1]) + "    " + str(i[2:]) + "\n")

file0.close()
print "Commiters, date and commited files are written to 'Group3_Commits.txt'"

#to find total commits
total_commit = 0
for i in user_list.values():
    total_commit += i

print "Number of commits is {}".format(total_commit)
#calculating %80 of total commit
top_developer = (total_commit * 80) / 100

#user list sorted by number of commit descending
user_list = sorted(user_list.items(), key=operator.itemgetter(1), reverse=True)

flag = 0
top_developer_list = []
file1 = open("Group3_Top_Developer_List.txt", "w")

#to print top developer's name
for i in range(len(user_list)):
    flag += user_list[i][1]
    if flag >= top_developer:
        break
    else:
        file1.write(user_list[i][0] + "\n")
        top_developer_list.append(user_list[i][0])

file1.close()

print "Number of top developers {}".format(len(top_developer_list))
print  "Names of top developer are written to 'Group3_Top_Developer_List.txt'"

file_list = []
for i in range(len(commit_list)):
    for j in range(2, len(commit_list[i])):
        if commit_list[i][j] in file_list:
            continue
        else:
            file_list.append(commit_list[i][j])

contributer_list = []
for i in range(len(commit_list)):
    if commit_list[i][0] in contributer_list:
        continue
    else:
        contributer_list.append(commit_list[i][0])

files_of_author = []
for i in range(len(contributer_list)):
    files_of_author.append([contributer_list[i]])
    for j in range(len(commit_list)):
        if files_of_author[i][0] == commit_list[j][0]:
            files_of_author[i].extend(commit_list[j][2:])

author_index = []
file_index = []

for i in range(len(contributer_list)):
    author_index.append([contributer_list[i]])
    author_index[i].extend([i])

for i in range(len(file_list)):
    file_index.append([file_list[i]])
    file_index[i].extend([i])

matrix = [[0 for x in range(len(file_list))] for y in range(len(contributer_list))]



def GetIndexFile(file_name):
    for i in range(len(file_index)):
        if file_index[i][0] == file_name:
            return i

def GetIndexAuthor(author_name):
    for i in range(len(author_index)):
        if author_index[i][0] == author_name:
            return i

matrix_i = 0
matrix_j = 0

for i in range(len(files_of_author)):
    matrix_i = GetIndexAuthor(files_of_author[i][0])
    for j in files_of_author[i][1:]:
        matrix_j = GetIndexFile(j)
        matrix[matrix_i][matrix_j] = 1

file2 = open("Matrix.txt", "w")
for i in author_index:
    file2.write(str(i[1]) + "\t" + str(i[0]) + "\n")

file2.write("="*50 + "\n\n")

for i in file_index:
    file2.write(str(i[1]) + "\t" + str(i[0]) + "\n")

file2.write("="*50 + "\n\n")

for i in range(len(contributer_list)):
    file2.write(str(matrix[i]) + "\n" + "\n")

file2.close()

user_list = dict(user_list)

#Plot the distrubition of commits in terms each developer
plt.bar(range(len(user_list)), user_list.values(), align='center')
plt.xticks(range(len(user_list)), user_list.keys())
plt.savefig("Distribution.png")
plt.show()

print "Close the window of first graphic to show 'visualization of socio-technical network' graph."

print "Distrubition of commits in terms each developer graph is printed to screen."

#Visualization of socio-technical network
G = NX.Graph()
for commit in repo.get_commits():
    authorOfCommit = commit.commit.author
    if authorOfCommit.name in top_developer_list:
        if str(authorOfCommit.date) > first_commit_date:
            for parent in commit.parents:
                G.add_edge(parent.sha, commit.sha)
        else:
            break

NX.draw(G, cmap = plt.get_cmap('jet'), node_color = 'b')
plt.savefig("Network.png")
plt.show()
