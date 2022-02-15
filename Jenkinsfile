groovy
// This is just to generate the pretend we are building, doesn't build anything
@Library('stuart-jenkins-pipelines@juan-SYS-2753-argocd-groovy-scripts') _

pipeline {
    agent {
      label 'slave-ireland'
    }
    environment {
        slackNotificationChannel = "deploys"
    }

    options {
        buildDiscarder(logRotator(daysToKeepStr: '20', numToKeepStr: '100'))
        timestamps()
        timeout(time: 3, unit: 'HOURS')
    }

    stages {
        stage('Abort previous build if running') {
            steps {
                script {
                    common.abortPreviousRunningBuilds()
                }
            }
        }
        stage('Self commit check') {
            steps {
		script {
		    //checkout([$class: 'GitSCM', branches: [[name: '*/juan-SYS-2522-prometheus-helm-argoCD']], extensions: [], userRemoteConfigs: [[credentialsId: '3db58f3d-60a0-4c7a-a9d2-4c3f98c1b07a', url: 'https://github.com/StuartApp/argocd-mini-prometheus/']]])
		    if (lastCommitIsSelfCommit()) {
		        currentBuild.result = 'NOT_BUILT'
		        error('Last commit was self triggered byt this pipeline, aborting the build to prevent a loop.')
		    } else {
		        echo('Last commit was not selftrigger , job continues as normal.')
		    }
               }
           }
       }

        stage('Prepare environment') {
            steps {
                script {
                    projectName = "requestbin"
                    image_version = env.GIT_COMMIT
                 }
            }
        }

        stage('Images and artifacts') {
            steps{
                /*script {
                    withCredentials([
                        [ $class: 'UsernamePasswordMultiBinding',
                        credentialsId: 'b4146a0c-999d-48ee-8745-0e4d478d7363',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY' ]
                      ]) {
                        bakeWithPublicDockerImage("stuartdevops/sftp-to-s3:${image_version}", projectName, env.GIT_COMMIT)
                        slackNotification("${projectName} AMI built successfully. We will now deploy it with Spinnaker.", slackNotificationChannel, 'green')
                    }
                }*/
                echo('build your docker image here, and push it somewhere nice')
            }
        }

	stage('Deploy to ArgoCD') {
	    steps{
		//withCredentials([gitUsernamePassword(credentialsId: '3db58f3d-60a0-4c7a-a9d2-4c3f98c1b07a', gitToolName: 'Default')]) {
		/// This would only happen for develop or master
		deployToArgo('3db58f3d-60a0-4c7a-a9d2-4c3f98c1b07a',projectName+"-"+image_version)
	    }
	}

    }

    post {
        always {
            script {
                //notifyBuild(currentBuild.result, env.slackNotificationChannel)
		echo('You can notify here')
            }
        }
    }
}
