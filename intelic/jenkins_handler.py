from django.conf import settings
from jenkinsapi.jenkins import Jenkins
from pprint import pprint

class JenkinsErrorException(Exception):
  pass

class JenkinsHandler(object):
    def __init__(self, host, username, password, *kwargs):
        """
        Initial the build and download jobs
        """
        self.server = Jenkins(host, username, password)
        self.job = self.server[settings.JENKINS_BUILD_JOB_NAME]
        self.invoke = None
        self.build = None
        
    def trigger(self, params):
        """
        Trigger actions
        
        Returns jenkinsapi.invocation.Invocation
        """
        self.invoke = self.job.invoke(build_params=params)
        return self.invoke

    def get_build(self, id):
        """
        Get the build instance
        """
        self.build = self.job.get_build(id)
        return self.build

    def get_build_id(self):
        """
        Get the build ID
        """
        return self.invoke.get_build_number() + 1

    def get_build_log(self):
        return self.build.baseurl + '/console'
    
    def get_build_results(self):
        artifacts = self.build.get_artifact_dict()
        for key in artifacts:
            return artifacts[key].url
    
    def is_complete(self):
        if self.build.is_running():
            return 0, 'Building'
        elif not self.build.is_good():
            return 500, 'Failure'
        return 200, 'Success'
