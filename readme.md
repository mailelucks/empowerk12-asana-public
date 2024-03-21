# Custom Asana API Application

## Criteria

Pull data from Asana following specific parameters and post to the EmpowerK12 database.

## Development Intent

- The app tasks are not separated out into smaller components/helpers due to the custom nature of project and task setup within Asana. I noticed that the client had different setups throughout their data, thus I decided to keep a lot of the logic static.
- Docker was necessary for me to build the application due to hardware issues on the device that I was using to build, a 2015 Macbook Pro that used an Intel chip. I am unsure if there are other quirks with this build that may break when loading the app onto Windows or Macs that use Apple silicon chips.
