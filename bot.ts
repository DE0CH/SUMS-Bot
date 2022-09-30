import { Client, GatewayIntentBits, SlashCommandBuilder, Routes, Role, GuildMemberRoleManager, SlashCommandRoleOption } from 'discord.js';
import { REST } from '@discordjs/rest';
import { clientId, token } from "./config";

const commands = [
  new SlashCommandBuilder().setName('ping').setDescription('Replies with pong!'),
  new SlashCommandBuilder()
	.setName('get_role')
	.setDescription('get a role')
	.addStringOption(option =>
		option.setName('role')
    .setDescription('The role you want to get')
			.setRequired(true)
			.addChoices(
        { name: 'St Andrews', value: '1012857848113418240' },
        { name: 'Edingbrugh', value: '1012891277701943356' },
        { name: 'Herrior Watt', value: '1012891421306527844'}, 
        { name: 'Aberdeen', value: '1012891550684033094'},
        { name: 'Glasgow', value: '1012891588726366209' }
			)),
  new SlashCommandBuilder()
  .setName('remove_role')
  .setDescription('remove a role')
  .addStringOption(option =>
    option.setName('role')
    .setDescription('The role you want to remove')
      .setRequired(true)
      .addChoices(
        { name: 'St Andrews', value: '1012857848113418240' },
        { name: 'Edingbrugh', value: '1012891277701943356' },
        { name: 'Herrior Watt', value: '1012891421306527844'}, 
        { name: 'Aberdeen', value: '1012891550684033094'},
        { name: 'Glasgow', value: '1012891588726366209' }
      )),
]
	.map(command => command.toJSON());

const rest = new REST({ version: '10' }).setToken(token);

const guildId = "1012857752743325827";

rest.put(Routes.applicationGuildCommands(clientId, guildId), { body: commands })
	.then(() => console.log('Successfully registered application commands.'))
	.catch(console.error);


// Create a new client instance
const client = new Client({ intents: [
  GatewayIntentBits.Guilds] });

// When the client is ready, run this code (only once)
client.once('ready', () => {
	console.log('Ready!');
});

// Login to Discord with your client's token
client.login(token);
client.on('interactionCreate', async interaction => {
  try {
  if (!interaction.isChatInputCommand()) return;
  if (interaction.guildId != guildId) {await interaction.reply(`Command not supported.`); return}

  const { commandName, member } = interaction;
  if (commandName === 'ping') {
		await interaction.reply('Pong!');
  } else if (commandName === 'get_role') {
    const role = interaction.guild?.roles.cache.get(interaction.options.getString('role')!);
    (member?.roles as GuildMemberRoleManager).add(role!);
    await interaction.reply(`Successfully added your role`)
  } else if (commandName == 'remove_role') {
    const role = interaction.guild?.roles.cache.get(interaction.options.getString('role')!);
    (member?.roles as GuildMemberRoleManager).remove(role!);
    await interaction.reply(`Successfully removed your role`)
  }
} catch (e) {
  console.log(e)
}
});

client.login(token);