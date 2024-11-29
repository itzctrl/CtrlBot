########################################
#     Discord Bot made by ItzCtrl      #
#     Website: https://itzctrl.com     #  
#  GitHub: https://github.com/itzctrl  #
########################################


import discord
from discord import app_commands
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

panel_channels = {}
voice_channels = {}
user_channels = {}
ticket_channels = {}
support_roles = {}
user_tickets = {}

class ChannelControls(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔢", style=discord.ButtonStyle.primary, custom_id="set_limit", row=0)
    async def set_limit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SetLimitModal())

    @discord.ui.button(label="🔨", style=discord.ButtonStyle.danger, custom_id="kick_user", row=0)
    async def kick_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(KickUserModal())

    @discord.ui.button(label="🔒", style=discord.ButtonStyle.secondary, custom_id="lock_unlock", row=0)
    async def lock_unlock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_lock(interaction)

    @discord.ui.button(label="✏", style=discord.ButtonStyle.primary, custom_id="rename", row=1)
    async def rename(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RenameChannelModal())

    @discord.ui.button(label="🚫", style=discord.ButtonStyle.danger, custom_id="ban_user", row=1)
    async def ban_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BanUserModal())

    @discord.ui.button(label="👁️", style=discord.ButtonStyle.secondary, custom_id="toggle_visibility", row=1)
    async def toggle_visibility(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_toggle_visibility(interaction)

class SetLimitModal(discord.ui.Modal, title="Set User Limit"):
    limit = discord.ui.TextInput(label="New user limit (0 for no limit)", placeholder="Enter a number")

    async def on_submit(self, interaction: discord.Interaction):
        await handle_limit(interaction, self.limit.value)

class KickUserModal(discord.ui.Modal, title="Kick User"):
    user = discord.ui.TextInput(label="User to kick", placeholder="Enter user ID or @mention")

    async def on_submit(self, interaction: discord.Interaction):
        await handle_kick(interaction, self.user.value)

class RenameChannelModal(discord.ui.Modal, title="Rename Channel"):
    new_name = discord.ui.TextInput(label="New channel name", placeholder="Enter new name")

    async def on_submit(self, interaction: discord.Interaction):
        await handle_rename(interaction, self.new_name.value)

class BanUserModal(discord.ui.Modal, title="Ban User"):
    user = discord.ui.TextInput(label="User to ban", placeholder="Enter user ID or @mention")

    async def on_submit(self, interaction: discord.Interaction):
        await handle_ban(interaction, self.user.value)

class TicketPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.primary, custom_id="create_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await create_ticket(interaction)

class CloseTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await close_ticket(interaction)

    @discord.ui.button(label="Close with reason", style=discord.ButtonStyle.danger, custom_id="close_ticket_reason")
    async def close_with_reason(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CloseTicketModal())

class CloseTicketModal(discord.ui.Modal, title="Close Ticket"):
    reason = discord.ui.TextInput(label="Reason for closing", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await close_ticket(interaction, self.reason.value)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    if len(bot.guilds) <= 1:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} server!"))
    elif len(bot.guilds) > 1:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers!"))
    
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="setup-vc-panel", description="Set up the voice channel control panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_panel(interaction: discord.Interaction, text_channel: discord.TextChannel, voice_channel: discord.VoiceChannel):
    panel_channels[interaction.guild.id] = text_channel
    voice_channels[interaction.guild.id] = voice_channel
    
    embed = discord.Embed(title="Manage VC", description="🔢 - Set VC Limit\n🔨 - Kick User\n🔒 - Lock/Unlock VC\n:pencil2: - Rename VC\n🚫 - Ban User\n👁️ - Hide/Unhide VC")
    await text_channel.send(embed=embed, view=ChannelControls())
    await interaction.response.send_message(f"Panel set up in {text_channel.mention}. Main voice channel: {voice_channel.mention}", ephemeral=True)

@bot.tree.command(name="setup-ticket-panel", description="Set up the ticket panel")
@app_commands.checks.has_permissions(administrator=True)
async def setup_ticket_panel(interaction: discord.Interaction, channel: discord.TextChannel, support_role: discord.Role):
    support_roles[interaction.guild.id] = support_role
    embed = discord.Embed(title="Support Tickets", description="Click the button below to create a support ticket.")
    await channel.send(embed=embed, view=TicketPanel())
    await interaction.response.send_message("Ticket panel has been set up.", ephemeral=True)

async def create_ticket(interaction: discord.Interaction):
    guild = interaction.guild
    support_role = support_roles.get(guild.id)
    
    if not support_role:
        await interaction.response.send_message("Support role not set up. Please contact an administrator.", ephemeral=True)
        return

    if interaction.user.id in user_tickets:
        await interaction.response.send_message("You already have an open ticket. Please close your existing ticket before creating a new one.", ephemeral=True)
        return

    category = discord.utils.get(guild.categories, name="Tickets")
    if not category:
        category = await guild.create_category("Tickets", overwrites={
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            support_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        })

    channel_name = f"ticket-{interaction.user.name}"
    channel = await category.create_text_channel(channel_name, overwrites={
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        support_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    })

    embed = discord.Embed(title="New Support Ticket", description="Please wait for a staff member to assist you. In the meanwhile, describe your problem as best as you can.")
    await channel.send(embed=embed, view=CloseTicket())
    
    ticket_channels[channel.id] = interaction.user.id
    user_tickets[interaction.user.id] = channel.id
    await interaction.response.send_message(f"Ticket created in {channel.mention}", ephemeral=True)

async def close_ticket(interaction: discord.Interaction, reason: str = None):
    if interaction.channel.id not in ticket_channels:
        await interaction.response.send_message("This is not a ticket channel.", ephemeral=True)
        return

    user_id = ticket_channels[interaction.channel.id]
    user = interaction.guild.get_member(user_id)
    embed = discord.Embed(title="Ticket Closed", description=f"Ticket closed by: {interaction.user.mention}")
    
    if reason:
        embed.add_field(name="Reason", value=reason)
    else:
        embed.add_field(name="Reason", value="No reason provided")

    if user:
        try:
            await user.send(embed=embed)
        except discord.HTTPException:
            pass

    await interaction.channel.delete()
    del ticket_channels[interaction.channel.id]
    del user_tickets[user_id]

@bot.tree.command(name="give-role-all", description="Give a role to everyone on the server")
@app_commands.checks.has_permissions(administrator=True)
async def give_role_all(interaction: discord.Interaction, role: discord.Role):
    await interaction.response.defer()
    for member in interaction.guild.members:
        try:
            await member.add_roles(role)
        except discord.HTTPException:
            pass
    await interaction.followup.send(f"Role {role.name} has been given to all members.")

@bot.tree.command(name="remove-role-al", description="Remove a role from everyone on the server")
@app_commands.checks.has_permissions(administrator=True)
async def remove_role_all(interaction: discord.Interaction, role: discord.Role):
    await interaction.response.defer()
    for member in interaction.guild.members:
        try:
            await member.remove_roles(role)
        except discord.HTTPException:
            pass
    await interaction.followup.send(f"Role {role.name} has been removed from all members.")

@bot.tree.command(name="ban", description="Ban a user from the server")
@app_commands.checks.has_permissions(administrator=True)
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str = None):
    await user.ban(reason=reason)
    await interaction.response.send_message(f"{user.name} has been banned. Reason: {reason or 'No reason provided'}")

@bot.tree.command(name="kick", description="Kick a user from the server")
@app_commands.checks.has_permissions(administrator=True)
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = None):
    await user.kick(reason=reason)
    await interaction.response.send_message(f"{user.name} has been kicked. Reason: {reason or 'No reason provided'}")

@bot.tree.command(name="role", description="Add a role to a user")
@app_commands.checks.has_permissions(administrator=True)
async def role(interaction: discord.Interaction, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await interaction.response.send_message(f"Added role {role.name} to {user.name}")

@bot.tree.command(name="role-remove", description="Remove a role from a user")
@app_commands.checks.has_permissions(administrator=True)
async def role_remove(interaction: discord.Interaction, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await interaction.response.send_message(f"Removed role {role.name} from {user.name}")

bot.run('BOT-TOKEN')