<script>
	import '@evidence-dev/tailwind/fonts.css';
	import '../app.css';
	import { EvidenceDefaultLayout } from '@evidence-dev/core-components';
	export let data;
</script>

<EvidenceDefaultLayout {data}
	hideSidebar=true
	githubRepo="https://github.com/cybermaxs/github-stars-monitor/"
	title="GitHub Stars Monitor"
	builtWithEvidence=true>
	<slot slot="content" />
</EvidenceDefaultLayout>
