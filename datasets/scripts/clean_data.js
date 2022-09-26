const path = require('path');
const fs = require('fs');

const scriptsDir = path.dirname(path.resolve(__filename));
const rawDataDir = path.join(scriptsDir, '..', 'raw_data');

const seedVariety = [
	'NSIC RC 222',
	'NSIC RC 192',
	'NSIC RC 11',
	'NSIC RC 120',
	'NSIC RC 396',
	'NSIC RC 350',
	'NSIC RC 410',
	'NSIC RC 100',
	'NSIC RC 102',
	'NSIC RC 242',
	'NSIC RC 56',
	'NSIC RC 12',
	'NSIC RC 42',
	'NSIC RC 442',
	'NSIC RC 510'
];

// Set headers for new datasets
const cleanData = [
	'NSIC_C_222,NSIC_C_192,NSIC_C_11,NSIC_C_120,NSIC_C_396,NSIC_C_350,NSIC_C_410,NSIC_C_100,NSIC_C_102,NSIC_C_242,NSIC_C_56,NSIC_C_12,NSIC_C_42,NSIC_C_442,NSIC_C_510,Land_area,Max_rain,Max_Temp,Humidity,Seeds_qty,Tot_yield'
];

// Read files from raw_data directory
const files = fs.readdirSync(rawDataDir);

// Loop files from raw_data directory
for (const file of files) {
	const cleanDataFromFile = [];

	// Read csv file
	const data = fs.readFileSync(path.join(rawDataDir, file), {
		encoding: 'utf8',
		flag: 'r'
	});

	// Split data by every end line and remove headers
	for (const line of data.split('\n').splice(1)) {
		// Ignore empty lines
		if (line.trim() !== '') {
			// Remove first 3 columns
			const newLine = line.split(',').splice(2);
			// Verify if all values has data, if not, don't append new data
			if (newLine.every((value) => value)) {
				const seed = seedVariety.map((seed) => (seed === newLine[0] ? 1 : 0));
				newLine.shift();
				newLine.unshift(seed);
				cleanDataFromFile.push(newLine.join(','));
			}
		}
	}

	// Append new clean data
	cleanData.push(cleanDataFromFile.join('\n'));
}

// Join cleanData to a whole string
const newData = cleanData.join('\n');

// Write new csv file using the new datasets
const newFile = path.join(scriptsDir, '..', 'datasets.csv');
fs.writeFile(newFile, newData, (err) => {
	if (err) throw err;

	console.log('New dataset successfully saved!');
});
