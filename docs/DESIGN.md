## Motivation
The Massachusetts Bay Transit Authority (MBTA) is the public transit system serving Greater Boston and its surrounding areas. In March 2020, due to the COVID-19 pandemic, ridership plummeted and still has not returned to pre-pandemic levels. In February 2023, Chief Financial Officer Mary Ann O'Hara told the MBTA Board of Directors, "Fare revenue is now supporting less than one-quarter of operating expenses today." 

In fiscal 2024, the T (MBTA) projects that ratio [will be only 18.7% compared to 43% pre-pandemic](https://www.nbcboston.com/news/local/t-towns-fear-service-levels-will-never-recover-from-pandemic-forcing-higher-fares/3048664/), putting pressure on the government to offer more subsidies or the agency to either slash costs or raise fares.

According to the MBTA Advisory Board, "Fare increases reduce ridership, and the MBTA's mission must be to attract riders right now." 

Therefore, the T needs other ways to raise ridership. 

## Requirements

We will raise ridership by creating a new mobile app that will satisfy the following sets of requirements:

### User Experience 
* A set of audio tours in partnership with the MBTA
* Accessible via a free mobile application – user downloads the app for free
* There would be at least one tour per route
* Each tour would focus on sites visible from the windows or within walking distance from stops, especially in the case of the subway portions of the routes
* The content of the tours would be a mixture of crowd-sourced audio clips from Bostonians and clips produced by a MONUM staff member.  (add crowd-sourced content, fact-checked by a MONUM staffer.) 
* Audio is accompanied by a visual, an address, and transcription
* The clips will be rotated out on the first day of each month.

### Frontend  
* User is able to search for different routes
* Home page displays tours near you
* Audio begins to play when a user enters one of the locations defined in the tour 
* A photo will appear along with the audio accompanied by brief text description and information about location and audio author 
* User should access to full audio player 
* When the user hits pause, the audio pauses
* When the user hits play,
    If the user has not finished current audio, it finishes current audio despite location
    If the user finished last audio, it begins playing the next available audio based on their location 
* The user can enable or disable autoplay by pressing a button. When autoplay is enabled, the following happens:
  * If the user is not playing any audio and they enter the “start zone” for an audio file, that audio will start playing
  * If they are playing audio and they enter the start zone for a different audio file, that audio will not start playing until the current audio is complete
* User is able to view a list of all stories associated with tour (preview route)
* User can view a zoomable map. The map shows their location and the different points along the route, connected by a thick line
* User is given the option to upload stories and provide
  * Name
  * Audio
  * Images
  * Address of location
  * Email
* Transcription available for audio tours
* Monum staff member should be able to:
  * Upload new content
  * Approve content 
  * Create new tours

### Backend 
* Store audio files and images
* Make approved content accessible and unapproved content non-accessible
* Retrieve audio files, associated images, and metadata based on GPS coordinates
* Enable search for a route
* Retrieve tours near a GPS location
* Retrieve data of all tour stops on a given route

## High-Level Solution

This mobile application can satisfy the requirements by providing bus riders with fact-checked stories from local Bostonians. The application will automatically play audio that syncs with landmarks visible from the rider's current position. Users can submit new stories, which will be reviewed by MONUM staff and either added to a tour or rejected. The stories will be stored on the backend.

This is a POC (Proof of Concept) of this app. 

### Web App vs. Mobile App

A mobile app provides a better user experience:
 * Users access the app by tapping on an easy-to-remember icon versus having to remember a   URL
 * Users can access the audio content offline

Mobile apps support both iOS and Android separately, which adds development time. The benefits outweigh this extra expense. 

### Serverless vs. Monolith

This project uses AWS API Gateway, AWS Lambda, AWS S3, and AWS DynamoDB to implement a serverless backend architecture. Alternatively, we could use EC2 with S3 and DynamoDB. Serverless has a number of advantages:

* Lambda will only execute when we need it to so that we don't have to pay for EC2 servers to sit idle; this makes serverless cheaper.
* Serverless architecture is kept up-to-date by AWS for us.
* * This means we have no downtime from kernel updates and expend no effort in software updates and version management.
* EC2 instances can crash, and we have to spend more development time to handle potential crashes. Serverless does not have this problem. 

### NoSQL vs. SQL

The data is easily modeled through a JSON structure, which is natively supported by a NoSQL database.  

## API Design

### Definitions

* Route - the path defined by MBTA
  * A route has at least one tour
  * Every tour lies along a bus route 
  * One tour per route
* Tour - a collection of locations and their associated audio; a mapping from location to audio 

### Data Types


### Methods
* `getRoute(routeName: string): Route`
* `getTour(routeName:string):Array<TourStop>`
* `getTourStop(location: GpsCoordinate): TourStop`
* `toursNearLocation(location: GpsCoordinate): Array<Route>`
* `routeSearch(query: string): Array<Route>` 

### Data Model

## Architecture


### Components 

## Future Work

## Some Thoughts
