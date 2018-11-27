
from DataParser import DataParser


from BM25 import BM25


def calculateJob(queryVector, docVector):
    bm25 = BM25()
    bm25.init_param(docVector, queryVector)
    result = bm25.mainprocess()
    return result


def subteskC(org_questions, all_comments):
    # loop get each question
    for eachorgquestion in org_questions.keys():
        each_orgquestion_id = eachorgquestion
        each_orgquestion_content = org_questions[eachorgquestion]
        rel_comment_list = []
        rel_comment_ID_list = []
        for eachRelComment in all_comments.keys():
            if each_orgquestion_id in eachRelComment:
                rel_comment_list.append(all_comments[eachRelComment])
                rel_comment_ID_list.append(eachRelComment)

        results = calculateJob([each_orgquestion_content], rel_comment_list)
        # process result
        count = 0

        f = open("subtaskC.pred", "a")
        for each_result in results:
            print(str(each_orgquestion_id) + " " + str(rel_comment_ID_list[count]) + " " + str(count) + " " + str(
                each_result) + " " + " false")
            f.write(str(each_orgquestion_id) + " " + str(rel_comment_ID_list[count]) + " " + str(count) + " " + str(
                each_result) + " " + " false")
            f.write("\n")
            count = count + 1


def subteskB(org_questions, rel_questions):
    # loop get each question
    for eachOrgquestion in org_questions.keys():
        orgQuestionID = eachOrgquestion
        rel_question_list = []
        rel_question_ID_list = []
        for eachRelQuestion in rel_questions.keys():
            if (orgQuestionID in eachRelQuestion):
                rel_question_list.append(rel_questions[eachRelQuestion])
                rel_question_ID_list.append(eachRelQuestion)

        results = calculateJob([org_questions[orgQuestionID]], rel_question_list)
        # process result
        count = 0
        f = open("subtaskB.pred", "a")
        for eachResult in results:
            print(
                orgQuestionID + " " + str(rel_question_ID_list[count]) + " " + str(count) + " " + str(
                    eachResult) + " false")
            f.write(
                orgQuestionID + " " + rel_question_ID_list[count] + " " + str(count) + " " + str(eachResult) + " false")
            f.write("\n")
            count = count + 1


def subtaskA(relcommtents, relquests):
    for each_rel_request in relquests:

        relQuestion = ""
        relQuestion_Content = ""
        for requestContent in each_rel_request:
            relQuestion = requestContent
            relQuestion_Content = each_rel_request[requestContent]
        for eachrelQuest in relcommtents.keys():
            if (eachrelQuest == relQuestion):
                relcommtents_contents = relcommtents[eachrelQuest]
                relcommentIDs = []
                relcommtentContents = []
                for eachrelcommentID in relcommtents_contents:
                    relcommentIDs.append(eachrelcommentID)
                    relcommtentContents.append(relcommtents_contents[eachrelcommentID])

                results = calculateJob([relQuestion_Content], relcommtentContents)

                count = 0
                f = open("subtaskA.pred", "a")
                print("Result Size " + str(len(results)))
                for eachResult in results:
                    print(str(eachrelQuest) + "  " + str(relcommentIDs[count]) + "  " + str(count + 1) + " " + str(
                        eachResult) + "  false")
                    f.write(str(eachrelQuest) + "  " + str(relcommentIDs[count]) + "  " + str(count + 1) + " " + str(
                        eachResult) + "  false")
                    f.write("\n")

                    count = count + 1


if __name__ == '__main__':
    dataparser = DataParser()
    contents = dataparser.readData("datas/test_data/SemEval2017-task3-English-test-input.xml")

    #subtask A
    org_questions, all_comments = dataparser.parseSubtaskCData(contents)
    subteskC(org_questions, all_comments)

    # subtask B
    org_questions, rel_questions = dataparser.parseSubtaskBData(contents)
    subteskB(org_questions, rel_questions)

    # subtask C
    relcommtents, relquests = dataparser.parseSubtaskAData(contents)
    subtaskA(relcommtents,relquests)


