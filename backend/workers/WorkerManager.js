const Worker = require("./BedWorker");

const workers = new Map();

function startWorker(bed) {

  if (workers.has(bed._id.toString())) {
    console.log(`Worker already running for Bed ${bed.bedNumber}`);
    return;
  }

  const worker = new Worker(bed);

  worker.start();

  workers.set(
    bed._id.toString(),
    worker
  );

  console.log(`Started Worker : Bed ${bed.bedNumber}`);
}

function stopWorker(bedId) {

  const worker = workers.get(bedId);

  if (!worker)
    return;

  worker.stop();

  workers.delete(bedId);

  console.log(`Stopped Worker : ${bedId}`);
}

function restartWorker(bed) {

  stopWorker(
    bed._id.toString()
  );

  startWorker(bed);

}

function getWorker(bedId) {

  return workers.get(
    bedId
  );

}

function getWorkers() {

  return workers;

}

module.exports = {

  startWorker,
  stopWorker,
  restartWorker,
  getWorker,
  getWorkers

};