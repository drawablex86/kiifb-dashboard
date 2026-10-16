import publicValueData from '../../../data/processed/public_value_and_geography.json';
import kanakkuPackages from '../../../data/processed/kanakku_packages.json';
import manifestData from '../../../data/manifest.json';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return {
		publicValue: publicValueData,
		kanakkuPackages: kanakkuPackages.packages,
		manifest: manifestData
	};
};

