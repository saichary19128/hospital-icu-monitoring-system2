class BedWorker {

  constructor(bed) {

    this.bed = bed;

    this.running = false;

  }

  start() {

    this.running = true;

    console.log(
      `Worker Started -> Bed ${this.bed.bedNumber}`
    );

    console.log(
      `Stream : ${this.bed.streamUrl}`
    );

    // Next milestone:
    // Open Raspberry Pi stream
    // Capture frames
    // Send frames to Python
  }

  stop() {

    this.running = false;

    console.log(
      `Worker Stopped -> Bed ${this.bed.bedNumber}`
    );

  }

}

module.exports = BedWorker;