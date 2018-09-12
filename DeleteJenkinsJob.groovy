#Script to delete jenkins job from a file
#Author : jyoti.bhanot30@gmail.com

import hudson.model.*;
import jenkins.model.*
def blacklist = new File('/tmp/list.txt') as String[]

println "Jobs to be deleted:"
for (job in blacklist){
    println job
}

println ""

println "Jobs Deleted:"
def jobs = Jenkins.instance.items; 
for (job in jobs) {
  if (job.getFullName() in blacklist){
      println "Deleting Job: " + job.getFullName()
      job.delete()
  }
}

def jobs1 = Jenkins.instance.items;
println "Remaining Jobs: "
for (job in jobs1){
  println "Job: " + job.getFullName()
}

println ""
println "Done" 
