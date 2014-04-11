
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="shortcut icon" href="../../assets/ico/favicon.ico">

    <title>Machine Learning Final Report</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/carousel.css" rel="stylesheet">
    <link href="css/index.css" rel="stylesheet">
  </head>
<!-- NAVBAR
================================================== -->
  <body>
    <div class="navbar-wrapper">
      <div class="container">

        <div class="navbar navbar-inverse navbar-static-top" role="navigation">
          <div class="container">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="#">NBA Game Outcome Predictor</a>
            </div>
          </div>
        </div>

      </div>
    </div>


    <!-- Carousel
    ================================================== -->
    <div id="myCarousel" class="carousel slide" data-ride="carousel">
      <!-- Indicators 
      <ol class="carousel-indicators">
        <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
        <li data-target="#myCarousel" data-slide-to="1"></li>
        <li data-target="#myCarousel" data-slide-to="2"></li>
      </ol>-->
      <div class="carousel-inner">
        <div class="item active">
          <div class="container">
            <div class="carousel-caption">
              <h1>Northwestern University</h1>
              <p>
              EECS 349: Machine Learning<br/>
              Professor Doug Downey</p>
              <p><a class="btn btn-lg btn-primary" href="final_report.pdf" role="button">Link to Detailed Report</a></p>
            </div>
          </div>
        </div>
      </div>
      <!--<a class="left carousel-control" href="#myCarousel" data-slide="prev"><span class="glyphicon glyphicon-chevron-left"></span></a>
      <a class="right carousel-control" href="#myCarousel" data-slide="next"><span class="glyphicon glyphicon-chevron-right"></span></a>-->
    </div><!-- /.carousel -->



    <!-- Marketing messaging and featurettes
    ================================================== -->
    <!-- Wrap the rest of the page in another container to center all the content. -->

    <div class="container marketing">
        <!-- Three columns of text below the carousel -->
              <div class="row">
                <div class="col-lg-4">
                  <img src="img/" width="140px" height="140px" class="img-circle" alt="Generic placeholder image">
                  <h2></h2>
                  <p>@u.northwestern.edu</p>
                  <p><a class="btn btn-default" href="http://www.linkedin.com/profile/view?id=280466630&locale=en_US&trk=tyah&trkInfo=tas%3Ayuxi%2Cidx%3A1-1-1" role="button">View details &raquo;</a></p>
                </div><!-- /.col-lg-4 -->
                <div class="col-lg-4">
                  <img class="img-circle" src="img/" width="140px" height="140px" alt="Generic placeholder image">
                  <h2></h2>
                  <p>@u.northwestern.edu</p>
                  <p><a class="btn btn-default" href="http://www.linkedin.com/profile/view?id=233742377&locale=en_US&trk=tyah&trkInfo=tas%3Asai%2Cidx%3A2-1-2" role="button">View details &raquo;</a></p>
                </div><!-- /.col-lg-4 -->
                <div class="col-lg-4">
                   <img class="img-circle" src="img/" width="140px" height="140px" alt="Generic placeholder image">
                  <h2>Yang Zhang</h2>
                  <p>yangzhang2015@u.northwestern.edu</p>
                  <p><a class="btn btn-default" href="http://www.linkedin.com/profile/view?id=243675017&trk=nav_responsive_tab_profile_pic" role="button">View details &raquo;</a></p>
                </div><!-- /.col-lg-4 -->
              </div><!-- /.row -->
      


      <!-- START THE FEATURETTES -->

      <hr class="featurette-divider">
       <h2 class="featurette-heading">Motivation</h2>
        <p class="lead"><nbsp><nbsp><nbsp>Professional sports, along with sports betting and lottery have been affecting people’s life spiritually and financially for decades. Major, professional sports leagues such as the NBA, NFL, and MLB contain a significant amount of easily accessible data whose outcomes tend to be randomly distributed and offer attractive data for analytical purposes. Predicting the outcomes of sporting events represents a natural application for machine learning. Above all, machine learning can make hidden data trends come to surface, which will help coaches and management levels make better decisions and strategies. Moreover, precise game outcome prediction is also critical to sports bettors for obvious reasons. In a nutshell, people’s personal opinions, professional or not, may differ from what the data says and what the truth is. As a consequence, using machine learning on statistics has a big chance to beat the NBA odds for a competitive or financial advantage.
        </p>
        <p class="lead">  In this project, we analyzed the NBA game statistics and made predictions on game outcomes for the 2013-2014 season.
        </p>
        
        <h2 class="featurette-heading">Solution</h2>
        
<div class="row featurette">
        <div class="col-md-5">
           <img src="img/graph.png" width="400px" height="400px"  alt="Generic placeholder image">
        </div>
        <div class="col-md-7">
          <p class="lead">  A chisquare test was used to analyze a set of 140 attributes of team statistics to determine 
the subset of features to be used in the prediction models. Using a chisquare value of 0.05 as a cutoff, 20 features were then selected by this method.</p>
          <p class="lead">  We used Naive Bayes classifier and decision tree learning algorithms on our data set.We tried all possible classifiers on our data set and these two tended to perform well and also scaled well.Naive Bayes outperforms all classifiers clearly for our task.We used cross-validation with 10-folds for our validation strategy to validate our classifier.Then we used future data i.e data for this weeks matches as our test set and tested our model on it.The average accuracy observed for Naive Bayes was “68.25%”.Followed by Decision Tree with an average accuracy of “64.71%”.</p>
        </div>
      </div>
      <h2 class="featurette-heading">Conclusion</h2>
       <p class="lead"> Our accuracies prove that selecting attributes using learning algorithms perform well compared to expert knowledge.Even though there is a similarity in attributes chosen by algorithm and expert knowledge.
</p>
      <p class="lead">  Also from  the selected attributes and increasing in accuracy we noted two important features.Home team statistics play an important role in deciding who wins or not.As most of the attributes chosen are related to Home team’s performance.Data consists of 140 attributes taken from three different statistics “Home performance”,”Opponent performance” and “General Performance” statistics of a team. From our analysis we noticed that most of features selected are from “General Performance” statistic like “Defense rating”,”offense rating” etc.These inferences tends to seem right as these attributes tend to be more meaningful in determining the result.
</p>
    <!--   <div class="row featurette">
        <div class="col-md-7">
          <h2 class="featurette-heading">First featurette heading. <span class="text-muted">It'll blow your mind.</span></h2>
          <p class="lead">Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. Praesent commodo cursus magna, vel scelerisque nisl consectetur. Fusce dapibus, tellus ac cursus commodo.</p>
        </div>
        <div class="col-md-5">
          <img class="featurette-image img-responsive" data-src="holder.js/500x500/auto" alt="Generic placeholder image">
        </div>
      </div>

      <hr class="featurette-divider">

      <div class="row featurette">
        <div class="col-md-5">
          <img class="featurette-image img-responsive" data-src="holder.js/500x500/auto" alt="Generic placeholder image">
        </div>
        <div class="col-md-7">
          <h2 class="featurette-heading">Oh yeah, it's that good. <span class="text-muted">See for yourself.</span></h2>
          <p class="lead">Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. Praesent commodo cursus magna, vel scelerisque nisl consectetur. Fusce dapibus, tellus ac cursus commodo.</p>
        </div>
      </div>

      <hr class="featurette-divider">

      <div class="row featurette">
        <div class="col-md-7">
          <h2 class="featurette-heading">And lastly, this one. <span class="text-muted">Checkmate.</span></h2>
          <p class="lead">Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. Praesent commodo cursus magna, vel scelerisque nisl consectetur. Fusce dapibus, tellus ac cursus commodo.</p>
        </div>
        <div class="col-md-5">
          <img class="featurette-image img-responsive" data-src="holder.js/500x500/auto" alt="Generic placeholder image">
        </div>
      </div>

      <hr class="featurette-divider"> -->

      <!-- /END THE FEATURETTES -->


      <!-- FOOTER -->
      <footer>
        <p class="pull-right"><a href="#">Back to top</a></p>
        <p>&copy; 2014 Yuxi, Sai and Yang &middot;</p>
      </footer>

    </div><!-- /.container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/docs.min.js"></script>
  </body>
</html>
