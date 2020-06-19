import json
from typing import Dict
from src.messageboard.models import Message
import statistics
import json


class MessageBoardAPIWrapper:
    """
    Wrapper around the messageboard API

    http://localhost:8080/api/
    """

    def __init__(self):
        pass

    def num_messages(self) -> int:
        """
        Returns the amount of messages in the database
        """
        return len(Message.objects.get()); 

    def create_word_frequency(self, allMessages):
        """
        Utility for getting map of word count in messages
        """
        wordCount = {}
        for message in allMessages:
            for word in message:
                if word in wordCount:
                    wordCount[word] = wordCount[word] + 1
                else:
                    wordCount[word] = 1
        return wordCount

    def most_common_word(self) -> str:
        """
        Returns the most frequently used word in messages.
        """
        wordCount = create_word_frequency(Message.objects.all())
        return max(wordCount, key=wordCount.get)

    def avg_num_words_per_sentence(self) -> float:
        """
        Returns the average number of words per sentence.
        """
        wordCount = create_word_frequency(Message.objects.all())
        return mean(wordCount, key=wordCount.get)

    def avg_num_msg_thread_topic(self) -> Dict[str, float]:
        """
        Returns the average number of messages per thread, per topic.
        """
        topicThreadAvgs = {}
        for topic in Topic.objects.all():
            topicThreadAvgs[topic.title] = 0
            for thread in Thread.objects.filter(title=topic.title):
                numberOfMessagesInThread = len(Message.objects.filter(title=thread.title))
                topicThreadAvgs[thread.title]=numberOfMessagesInThread
                topicThreadAvgs[topic.title]=topicAvgs[topic.title]+numberOfMessagesInThread

        return 

    def _as_dict(self) -> dict:
        """
        Returns the entire messageboard as a nested dictionary.
        """
        forumDict = {}
        for topic in Topic.objects.all():
            threadList = []
            topicDict = {}
            for thread in Thread.objects.filter(title=topic.title):
                messagesList = []
                threadDict = {}
                for message in Message.objects.filter(thread=thread):
                    messageDict = {}
                    messageDict["content"] = message.content
                    messageDict["author_name"] = message.author_name
                    messageDict["created_date"] = message.created_date
                    messagesList.append(messageDict)
                threadDict["title"] = thread.title
                threadDict["topic"] = thread.topic
                threadDict["author_name"] = thread.author_name
                threadDict["created_date"] = thread.created_date
                threadDict["messages"] = messagesList
                threadList.append(threadDict)
            topicDict["title"] = topic.title
            topicDict["slug"] = topic.slug
            topicDict["threads"] = threadList
            forumDict[topic.slug] = topicDict

        return forumDict

    def to_json(self) -> None:
        """
        Dumps the entire messageboard to a JSON file.
        """
        with open("messageboard.json", "w") as f:
            f.write(json.dumps(self._as_dict(), indent=4))


def main():
    """
    Returns information about the messageboard application
    """

    messageboard = MessageBoardAPIWrapper()

    print(f"Total number of messages: {messageboard.num_messages()}")
    print(f"Most common word: {messageboard.most_common_word()}")
    print(
        f"Avg. number of words per sentence:"
        f"{messageboard.avg_num_words_per_sentence()}"
    )
    print(
        f"Avg. number of messages per thread, per topic:"
        f"{messageboard.avg_num_msg_thread_topic()}"
    )

    messageboard.to_json()
    print("Message Board written to `messageboard.json`")
    return


if __name__ == "__main__":
    main()
