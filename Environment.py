'''
Environment class to to initiate job scraping and interact with agents to drive clustering operations
Author : Mayuri Wadkar
'''

from Webscraper import *
from SingleLinkClusteringAgent import *
from Utils import *
from KmeansClusteringAgent import *
from Topic import *
from Cluster import *

class Environment:

    utils = Utils()
    jobs_fetched = []

    '''
    Function to initiate web scraping of jobs using three scrapers.
    '''
    def start_webscraping_jobs(self):

        scraper = Webscraper()
        scraper.run_stackoverflow_scraper()
        scraper.run_dice_scraper()
        scraper.run_indeed_scraper()
        self.jobs_fetched = Webscraper.jobs_fetched
        print '\nTotal number of jobs fetched: '+str(len(self.jobs_fetched))

    '''
    Function to initiate clustering on jobs fetched
    '''
    def initiate_clustering(self):

        while(True):
            try:
                number_of_clusters = raw_input("Enter number of clusters: ")
                number_of_clusters = int(number_of_clusters)
                if number_of_clusters > len(self.jobs_fetched):
                    print 'Number of clusters cannot be greater than total number of jobs fetched.'
                else:
                    break
            except:
                print "Invalid input. Please try again."

        job_documents = []

        for job in self.jobs_fetched:
            desc = " ".join(job.summary)
            job_documents.append(desc)

        # for doc in job_documents:
        #     print doc+"\n\n"

        kmeans = KmeansClusteringAgent(self.jobs_fetched)
        clusters, closest = kmeans.start(job_documents, number_of_clusters)

        clusters_obj_list = []
        for index,cluster in clusters.items():
            cl = Cluster()
            cl.cluster_id = index
            cl.cluster = cluster
            cl.closest_job_document = self.jobs_fetched[closest[index]]

            print "\nCluster" + str(cl.cluster_id) + "--------------------------"
            for job in cl.cluster:
                print "\t" + job.jobTitle.encode('ascii', 'ignore')
            print "\n Job closest to centroid in cluster "+str(cl.cluster_id)+": \n"
            cl.closest_job_document.printDetails()
            clusters_obj_list.append(cl)

        while (True):
            try:
                number_of_clusters_for_nlp = raw_input("\n\nEnter number of course topics to generate: ")
                number_of_clusters_for_nlp = int(number_of_clusters_for_nlp)
                if (number_of_clusters_for_nlp > number_of_clusters):
                    print 'Enter a number less than the number of clusters.'
                else:
                    break
            except:
                print "Invalid input. Please try again."

        print 'Below are '+str(number_of_clusters_for_nlp)+' clusters built using Kmeans in descending order of size of cluster'
        final_clusters_for_nlp = []
        topics = []
        count = 0
        for k in sorted(clusters, key=lambda k: len(clusters[k]), reverse=True):
            count += 1
            print "\nCluster" + str(k) + "---------------"

            for cluster_obj in clusters_obj_list:
                if cluster_obj.cluster_id == k:
                    final_clusters_for_nlp.append(cluster_obj)

                    print 'Initiating single-link hierarchical clustering on Cluster ' + str(k)
                    single_link_clustering_agent = SingleLinkClusteringAgent()
                    single_link_clustering_agent.cluster = cluster_obj
                    parent_job = single_link_clustering_agent.start()

                    cluster_obj.parent_job_from_single_link = parent_job

                    print 'Parent job from hierarchy:'
                    cluster_obj.parent_job_from_single_link.printDetails()

                    print 'Fetching course topic and contents..'
                    topic = Topic()
                    topic.cluster = cluster_obj
                    topic.set_syllabus_content()
                    topics.append(topic)

                    print 'Topic fetched..'
                    break


            if count == number_of_clusters_for_nlp:
                break

        print '\n\nRecommended Topics----------------------------'
        for topic in topics:

            print ("\nTopic: -----------------------------------------------------------------------------------")
            print ("Topics in " + topic.topic + "\n")
            print ("Course Description: ----------------------------------------------------------------------")
            print ("Introduction to topics in " + topic.topic + " such as " + str(topic.technologies) + str(topic.listedTech))

            print ("\nCourse Learning Outcomes: -----------------------------------------------------------------")
            print topic.actionList
            print ('Summary:')
            print (topic.summary.encode('ascii', 'ignore'))
            print ("\n")

            self.utils.generate_pdf(topic)
















