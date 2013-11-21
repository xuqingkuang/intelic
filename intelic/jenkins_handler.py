from django.conf import settings
from jenkinsapi.jenkins import Jenkins

class ICJenkinsJob(Jenkins):
    def trigger_build(self, parameters):
        return self.build_job(settings.JENKINS_BUILD_JOB_NAME, parameters)

    def trigger_package(self, parameters):
        return self.build_job(settings.JENKINS_DOWNLOAD_JOB_NAME, parameters)

if settings.JENKINS_HOST:
    icjenkinsjob = ICJenkinsJob(
        settings.JENKINS_HOST, settings.JENKINS_USERNAME,
        settings.JENKINS_PASSWORD
    )
else:
    icjenkinsjob = None
