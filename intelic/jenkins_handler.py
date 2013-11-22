from django.conf import settings
from jenkinsapi.jenkins import Jenkins

class ICJenkinsJob(object):
    def __init__(self, host, username, password, *kwargs):
        """
        Initial the build and download jobs
        """
        self.server = Jenkins(host, username, password)
        self.build_job_instance = self.server[settings.JENKINS_BUILD_JOB_NAME]
        self.download_job_instance = self.server[settings.JENKINS_DOWNLOAD_JOB_NAME]
    
    def trigger_build(self, parameters):
        """
        Trigger the build action
        
        Returns jenkinsapi.invocation.Invocation
        """
        return self.build_job_instance.invoke(build_params=parameters)

    def trigger_package(self, parameters):
        """
        Trigger the package action
        
        Returns jenkinsapi.invocation.Invocation
        """
        return self.download_job_instance.invoke(build_params=parameters)

if settings.JENKINS_HOST:
    icjenkinsjob = ICJenkinsJob(
        settings.JENKINS_HOST, settings.JENKINS_USERNAME,
        settings.JENKINS_PASSWORD
    )
else:
    icjenkinsjob = None
