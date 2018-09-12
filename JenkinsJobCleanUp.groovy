#Script to clean up jenkins jobs that are not executed from last n days
#In our case n=180
#Author : jyoti.bhanot30@gmail.com

import hudson.model.*;
import jenkins.model.*
Calendar monthAgo = Calendar.getInstance();
monthAgo.add(Calendar.DATE, -180);
Jenkins.instance.getAllItems(AbstractProject.class).each {p ->
  if ( !p.getLastBuild() || p.getLastBuild().getTimestamp().compareTo(monthAgo) < 0)
    println p.getFullName() + ':'+ p.getLastBuild()?.getTimestampString()
}
