<h1>Pi-hole Adlists Repository</h1>
<p>Welcome to the Pi-hole Adlists Repository! This repository contains a curated collection of various adlists that you can use with Pi-hole, a network-wide ad blocker that runs on your Raspberry Pi or Linux server. By adding these adlists to your Pi-hole configuration, you can enhance your ad blocking capabilities and enjoy a cleaner browsing experience.</p>

<h2>How to Use</h2>
<p>To use these adlists with Pi-hole, follow these steps:</p>
<ol>
  <li><strong>Clone the Repository:</strong> Clone this repository to your local machine or server where Pi-hole is installed.</li>
  <pre><code>git clone https://github.com/yuneshwaran/pihole-adlists.git</code></pre>
  <li><strong>Add Adlists to Pi-hole:</strong> Add the adlists from this repository to your Pi-hole configuration. You can do this by navigating to your Pi-hole's web interface, clicking on "Group Management" &gt; "Adlists", and then adding each adlist URL manually or by using the command-line interface.</li>
  <pre><code>pihole -g</code></pre>
  <li><strong>Update Gravity:</strong> After adding the adlists, update Pi-hole's gravity to apply the changes and block the ads from the added lists.</li>
  <pre><code>pihole -g</code></pre>
  <li><strong>Optional: Regularly Update Adlists:</strong> It's recommended to regularly update the adlists in your Pi-hole configuration to ensure that you're blocking the latest ad domains and trackers.</li>
</ol>

<h2>Sources</h2>
<p> 
<a href="https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts">Stock list</a>
<a href="https://oisd.nl/">OISD</a>
<a href="https://github.com/lightswitch05/hosts">DeveloperDan</a>
<a href="https://github.com/blocklistproject/Lists">BlocklistProjects</a>
</p>

<h2>Disclaimer</h2>
<p>Please note that while these adlists are curated to block advertisements and trackers, they may also block legitimate content on some websites. Use them at your own discretion. Additionally, Pi-hole is a powerful tool, but it's not a silver bullet for blocking all ads and trackers. Some ads may still get through, especially those served from the same domain as the content you're trying to access.</p>