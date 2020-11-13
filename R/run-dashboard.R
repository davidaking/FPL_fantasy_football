
library(rmarkdown)

# Set up directories
current_user <- Sys.info()[["user"]]
dir_file <- paste0("c:\\users\\",current_user,"\\project-directories.csv")
project_dir = read.csv(dir_file)

project_name <- "FPL_fantasy_football"
row_ind <- project_dir$Project == project_name
project_dir <- project_dir[row_ind,,drop=F]




for (i in 1:nrow(project_dir)){
  
  dir_str <- paste(project_dir[i,],collapse="/")
  sub_dir_str <- tolower(project_dir[i,"directory"])
  text_str <- paste0(sub_dir_str,"_dir <- ","'",paste0("c:/users/",current_user,"/",dir_str,"/","'"))  
  eval(parse(text=text_str))
  
  
}


# render output
render(paste0(r_dir,"markdown.Rmd"),output_file = paste0(output_dir,"FPL-dashboard.html"))



